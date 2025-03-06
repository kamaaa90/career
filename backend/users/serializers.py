from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Notification, UserPreference, SavedService, SavedPackage


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active']
        read_only_fields = ['date_joined', 'is_active']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'profile_picture', 'phone_number', 'job_title', 
            'company', 'industry', 'years_of_experience', 'linkedin_url', 
            'website_url', 'twitter_url', 'address_line1', 'address_line2', 
            'city', 'state', 'postal_code', 'country', 'timezone', 'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for the Notification model."""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'title', 'message', 'notification_type', 'related_object_id',
            'related_object_type', 'is_read', 'created_at'
        ]
        read_only_fields = ['created_at']


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for the UserPreference model."""
    
    class Meta:
        model = UserPreference
        fields = [
            'id', 'user', 'email_notifications', 'sms_notifications', 
            'newsletter_subscription', 'marketing_emails', 'theme_preference',
            'language_preference', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SavedServiceSerializer(serializers.ModelSerializer):
    """Serializer for the SavedService model."""
    
    class Meta:
        model = SavedService
        fields = ['id', 'user', 'service', 'notes', 'created_at']
        read_only_fields = ['created_at']


class SavedPackageSerializer(serializers.ModelSerializer):
    """Serializer for the SavedPackage model."""
    
    class Meta:
        model = SavedPackage
        fields = ['id', 'user', 'package', 'notes', 'created_at']
        read_only_fields = ['created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
            
        return attrs

    def create(self, validated_data):
        # Remove password2 from validated data
        validated_data.pop('password2')
        
        # Create user
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Create default user preferences
        UserPreference.objects.create(user=user)
        
        return user


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for password reset confirmation."""
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
