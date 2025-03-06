from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import UserProfile, Notification, UserPreference, SavedService, SavedPackage
from .serializers import (
    UserSerializer, UserProfileSerializer, NotificationSerializer, 
    UserPreferenceSerializer, SavedServiceSerializer, SavedPackageSerializer,
    RegisterSerializer, PasswordChangeSerializer, PasswordResetSerializer,
    PasswordResetConfirmSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for the UserProfile model."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        """Allow users to view their own profile."""
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Notification model."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            return Notification.objects.all()
        return Notification.objects.filter(user=self.request.user)


class UserPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for the UserPreference model."""
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            return UserPreference.objects.all()
        return UserPreference.objects.filter(user=self.request.user)


class SavedServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for the SavedService model."""
    queryset = SavedService.objects.all()
    serializer_class = SavedServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            return SavedService.objects.all()
        return SavedService.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user to the current user."""
        serializer.save(user=self.request.user)


class SavedPackageViewSet(viewsets.ModelViewSet):
    """ViewSet for the SavedPackage model."""
    queryset = SavedPackage.objects.all()
    serializer_class = SavedPackageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        if self.request.user.is_staff:
            return SavedPackage.objects.all()
        return SavedPackage.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user to the current user."""
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    """View for user registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """View for user login."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            })
        
        return Response({
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """View for user logout."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Logout successful'
        })


class PasswordChangeView(APIView):
    """View for changing password."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'message': 'Old password is incorrect'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """View for requesting password reset."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Send email
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
                
                send_mail(
                    'Password Reset Request',
                    f'Please click the following link to reset your password: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                return Response({
                    'message': 'Password reset email sent'
                })
                
            except User.DoesNotExist:
                # We don't want to reveal which emails exist in our system
                pass
            
            return Response({
                'message': 'If an account with this email exists, a password reset link has been sent'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """View for confirming password reset."""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
                user = User.objects.get(pk=uid)
                
                # Check token
                if default_token_generator.check_token(user, serializer.validated_data['token']):
                    # Set new password
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    
                    return Response({
                        'message': 'Password reset successful'
                    })
                
                return Response({
                    'message': 'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            except (User.DoesNotExist, ValueError, TypeError, OverflowError):
                return Response({
                    'message': 'Invalid user ID'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """View for getting current user."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CurrentUserProfileView(APIView):
    """View for getting and updating current user's profile."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserPreferencesView(APIView):
    """View for getting and updating current user's preferences."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        preferences = UserPreference.objects.get(user=request.user)
        serializer = UserPreferenceSerializer(preferences)
        return Response(serializer.data)
    
    def put(self, request):
        preferences = UserPreference.objects.get(user=request.user)
        serializer = UserPreferenceSerializer(preferences, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserNotificationsView(APIView):
    """View for getting user's notifications."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class MarkNotificationReadView(APIView):
    """View for marking a notification as read."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            
            return Response({
                'message': 'Notification marked as read'
            })
            
        except Notification.DoesNotExist:
            return Response({
                'message': 'Notification not found'
            }, status=status.HTTP_404_NOT_FOUND)


class MarkAllNotificationsReadView(APIView):
    """View for marking all notifications as read."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        
        return Response({
            'message': 'All notifications marked as read'
        })


class UserSavedServicesView(APIView):
    """View for getting user's saved services."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        saved_services = SavedService.objects.filter(user=request.user).order_by('-created_at')
        serializer = SavedServiceSerializer(saved_services, many=True)
        return Response(serializer.data)


class UserSavedPackagesView(APIView):
    """View for getting user's saved packages."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        saved_packages = SavedPackage.objects.filter(user=request.user).order_by('-created_at')
        serializer = SavedPackageSerializer(saved_packages, many=True)
        return Response(serializer.data)
