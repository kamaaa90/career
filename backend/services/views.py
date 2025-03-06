from django.db.models import Q

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import ServiceCategory, Service, ServicePackage, ServiceFeature, Testimonial
from .serializers import (
    ServiceCategorySerializer, ServiceSerializer, ServicePackageSerializer,
    ServiceFeatureSerializer, TestimonialSerializer
)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the ServiceCategory model."""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = ServiceCategory.objects.all()
        
        # Filter active categories for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
            
        return queryset


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for the Service model."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions and query parameters."""
        queryset = Service.objects.all()
        
        # Filter active services for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name__in=[tag])
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(short_description__icontains=search)
            )
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def features(self, request, slug=None):
        """Get features for a service."""
        service = self.get_object()
        features = service.features.all()
        serializer = ServiceFeatureSerializer(features, many=True)
        return Response(serializer.data)


class ServicePackageViewSet(viewsets.ModelViewSet):
    """ViewSet for the ServicePackage model."""
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions and query parameters."""
        queryset = ServicePackage.objects.all()
        
        # Filter active packages for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(short_description__icontains=search)
            )
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def services(self, request, slug=None):
        """Get services included in a package."""
        package = self.get_object()
        services = package.services.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def features(self, request, slug=None):
        """Get features for a package."""
        package = self.get_object()
        features = package.features.all()
        serializer = ServiceFeatureSerializer(features, many=True)
        return Response(serializer.data)


class TestimonialViewSet(viewsets.ModelViewSet):
    """ViewSet for the Testimonial model."""
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on user permissions and query parameters."""
        queryset = Testimonial.objects.all()
        
        # Filter active testimonials for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Filter by service
        service_slug = self.request.query_params.get('service', None)
        if service_slug:
            queryset = queryset.filter(service__slug=service_slug)
        
        # Filter by package
        package_slug = self.request.query_params.get('package', None)
        if package_slug:
            queryset = queryset.filter(package__slug=package_slug)
            
        return queryset


class FeaturedServicesView(APIView):
    """View for getting featured services."""
    permission_classes = [AllowAny]
    
    def get(self, request):
        services = Service.objects.filter(is_featured=True, is_active=True)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class FeaturedPackagesView(APIView):
    """View for getting featured packages."""
    permission_classes = [AllowAny]
    
    def get(self, request):
        packages = ServicePackage.objects.filter(is_featured=True, is_active=True)
        serializer = ServicePackageSerializer(packages, many=True)
        return Response(serializer.data)


class FeaturedTestimonialsView(APIView):
    """View for getting featured testimonials."""
    permission_classes = [AllowAny]
    
    def get(self, request):
        testimonials = Testimonial.objects.filter(is_featured=True, is_active=True)
        serializer = TestimonialSerializer(testimonials, many=True)
        return Response(serializer.data)
