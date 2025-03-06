from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import ServiceCategory, Service, ServicePackage, ServiceFeature, Testimonial


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer for the ServiceCategory model."""
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'slug', 'icon', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']


class ServiceFeatureSerializer(serializers.ModelSerializer):
    """Serializer for the ServiceFeature model."""
    
    class Meta:
        model = ServiceFeature
        fields = ['id', 'name', 'description', 'icon', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ServiceSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializer for the Service model."""
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True
    )
    features = ServiceFeatureSerializer(many=True, read_only=True)
    tags = TagListSerializerField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'description', 'short_description', 'category', 
            'category_id', 'price', 'duration', 'image', 'features', 'is_featured', 
            'is_active', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


class ServicePackageSerializer(serializers.ModelSerializer):
    """Serializer for the ServicePackage model."""
    services = ServiceSerializer(many=True, read_only=True)
    service_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='services',
        write_only=True,
        many=True
    )
    features = ServiceFeatureSerializer(many=True, read_only=True)
    feature_ids = serializers.PrimaryKeyRelatedField(
        queryset=ServiceFeature.objects.all(),
        source='features',
        write_only=True,
        many=True
    )
    
    class Meta:
        model = ServicePackage
        fields = [
            'id', 'name', 'slug', 'description', 'short_description', 'price', 
            'discounted_price', 'duration', 'image', 'services', 'service_ids',
            'features', 'feature_ids', 'is_featured', 'is_active', 'created_at', 
            'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


class TestimonialSerializer(serializers.ModelSerializer):
    """Serializer for the Testimonial model."""
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True,
        required=False,
        allow_null=True
    )
    package = ServicePackageSerializer(read_only=True)
    package_id = serializers.PrimaryKeyRelatedField(
        queryset=ServicePackage.objects.all(),
        source='package',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'client_title', 'client_company', 'client_image',
            'content', 'rating', 'service', 'service_id', 'package', 'package_id',
            'is_featured', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
    def validate(self, attrs):
        """Validate that at least one of service or package is provided."""
        service = attrs.get('service')
        package = attrs.get('package')
        
        if not service and not package:
            raise serializers.ValidationError(
                "At least one of service or package must be provided."
            )
            
        return attrs
