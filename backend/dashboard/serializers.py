from rest_framework import serializers
from django.contrib.auth.models import User
from services.serializers import ServiceSerializer, ServicePackageSerializer
from .models import Analytics, PageVisit, FinancialReport, ServicePerformance, PackagePerformance, UserActivity


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class AnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for the Analytics model."""
    
    class Meta:
        model = Analytics
        fields = [
            'id', 'date', 'visits', 'unique_visitors', 'page_views', 'bounce_rate',
            'average_session_duration', 'conversion_rate', 'source', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PageVisitSerializer(serializers.ModelSerializer):
    """Serializer for the PageVisit model."""
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = PageVisit
        fields = [
            'id', 'user', 'page_url', 'page_title', 'visit_datetime', 'ip_address',
            'user_agent', 'referrer', 'session_id', 'time_spent', 'created_at'
        ]
        read_only_fields = ['created_at']


class FinancialReportSerializer(serializers.ModelSerializer):
    """Serializer for the FinancialReport model."""
    
    class Meta:
        model = FinancialReport
        fields = [
            'id', 'report_date', 'period_type', 'total_revenue', 'total_orders',
            'average_order_value', 'refunds', 'net_revenue', 'payment_processing_fees',
            'taxes_collected', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ServicePerformanceSerializer(serializers.ModelSerializer):
    """Serializer for the ServicePerformance model."""
    service = ServiceSerializer(read_only=True)
    
    class Meta:
        model = ServicePerformance
        fields = [
            'id', 'service', 'report_date', 'period_type', 'views', 'bookings',
            'conversion_rate', 'revenue', 'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PackagePerformanceSerializer(serializers.ModelSerializer):
    """Serializer for the PackagePerformance model."""
    package = ServicePackageSerializer(read_only=True)
    
    class Meta:
        model = PackagePerformance
        fields = [
            'id', 'package', 'report_date', 'period_type', 'views', 'bookings',
            'conversion_rate', 'revenue', 'average_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for the UserActivity model."""
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'activity_datetime', 'description',
            'ip_address', 'related_object_id', 'related_object_type', 'created_at'
        ]
        read_only_fields = ['created_at']


class DashboardOverviewSerializer(serializers.Serializer):
    """Serializer for dashboard overview data."""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_services = serializers.IntegerField()
    total_packages = serializers.IntegerField()
    total_appointments = serializers.IntegerField()
    pending_appointments = serializers.IntegerField()
    completed_appointments = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    recent_orders = serializers.IntegerField()
    recent_signups = serializers.IntegerField()
    conversion_rate = serializers.FloatField()


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary data."""
    total_visits = serializers.IntegerField()
    total_unique_visitors = serializers.IntegerField()
    total_page_views = serializers.IntegerField()
    average_bounce_rate = serializers.FloatField()
    average_session_duration = serializers.FloatField()
    average_conversion_rate = serializers.FloatField()
    top_sources = serializers.ListField(
        child=serializers.DictField()
    )
    top_pages = serializers.ListField(
        child=serializers.DictField()
    )


class FinancialSummarySerializer(serializers.Serializer):
    """Serializer for financial summary data."""
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_orders = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_refunds = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    revenue_by_period = serializers.ListField(
        child=serializers.DictField()
    )
    orders_by_period = serializers.ListField(
        child=serializers.DictField()
    )
