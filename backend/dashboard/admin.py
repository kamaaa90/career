from django.contrib import admin
from django.utils.html import format_html
from .models import Analytics, PageVisit, FinancialReport, ServicePerformance, PackagePerformance, UserActivity

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'page_views', 'unique_visitors', 'bounce_rate', 'avg_session_duration_formatted')
    list_filter = ('date',)
    search_fields = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('date',)
        }),
        ('Metrics', {
            'fields': ('page_views', 'unique_visitors', 'bounce_rate', 'avg_session_duration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def avg_session_duration_formatted(self, obj):
        minutes, seconds = divmod(obj.avg_session_duration, 60)
        return f"{minutes}m {seconds}s"
    avg_session_duration_formatted.short_description = 'Avg. Session Duration'

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'date', 'views', 'unique_views')
    list_filter = ('date',)
    search_fields = ('path',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('path', 'date')
        }),
        ('Metrics', {
            'fields': ('views', 'unique_views')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('get_period_display', 'start_date', 'end_date', 'total_revenue', 'total_orders', 'avg_order_value', 'net_revenue')
    list_filter = ('period_type', 'start_date', 'end_date')
    search_fields = ('period_type', 'start_date', 'end_date')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'end_date'
    fieldsets = (
        (None, {
            'fields': ('period_type', 'start_date', 'end_date')
        }),
        ('Revenue', {
            'fields': ('total_revenue', 'refunds', 'net_revenue')
        }),
        ('Orders', {
            'fields': ('total_orders', 'avg_order_value')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_period_display(self, obj):
        return obj.get_period_type_display()
    get_period_display.short_description = 'Period'
    get_period_display.admin_order_field = 'period_type'

@admin.register(ServicePerformance)
class ServicePerformanceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'date', 'views', 'orders', 'revenue')
    list_filter = ('date',)
    search_fields = ('service_name',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('service_id', 'service_name', 'date')
        }),
        ('Metrics', {
            'fields': ('views', 'orders', 'revenue')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(PackagePerformance)
class PackagePerformanceAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'date', 'views', 'orders', 'revenue')
    list_filter = ('date',)
    search_fields = ('package_name',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('package_id', 'package_name', 'date')
        }),
        ('Metrics', {
            'fields': ('views', 'orders', 'revenue')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('get_user_display', 'action', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'session_id', 'ip_address', 'action')
    readonly_fields = ('timestamp', 'formatted_action_details')
    date_hierarchy = 'timestamp'
    fieldsets = (
        (None, {
            'fields': ('user', 'session_id', 'action')
        }),
        ('Details', {
            'fields': ('ip_address', 'formatted_action_details', 'timestamp')
        }),
    )
    
    def get_user_display(self, obj):
        if obj.user:
            return obj.user.username
        return f"Session: {obj.session_id[:10]}..."
    get_user_display.short_description = 'User'
    
    def formatted_action_details(self, obj):
        if not obj.action_details:
            return '-'
        html = '<dl>'
        for key, value in obj.action_details.items():
            html += f'<dt><strong>{key}</strong></dt><dd>{value}</dd>'
        html += '</dl>'
        return format_html(html)
    formatted_action_details.short_description = 'Action Details'
