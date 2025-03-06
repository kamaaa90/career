from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Analytics(models.Model):
    date = models.DateField(unique=True)
    page_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    avg_session_duration = models.PositiveIntegerField(default=0)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Analytics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"

class PageVisit(models.Model):
    path = models.CharField(max_length=255)
    views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['path', 'date']
        ordering = ['-date', '-views']
    
    def __str__(self):
        return f"{self.path} - {self.date}"

class FinancialReport(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refunds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['period_type', 'start_date', 'end_date']
        ordering = ['-end_date']
    
    def __str__(self):
        return f"{self.get_period_type_display()} Report: {self.start_date} to {self.end_date}"

class ServicePerformance(models.Model):
    service_id = models.PositiveIntegerField()  # Reference to Service model
    service_name = models.CharField(max_length=200)
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    orders = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['service_id', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.service_name} - {self.date}"

class PackagePerformance(models.Model):
    package_id = models.PositiveIntegerField()  # Reference to ServicePackage model
    package_name = models.CharField(max_length=200)
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    orders = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['package_id', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.package_name} - {self.date}"

class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view_service', 'View Service'),
        ('view_package', 'View Package'),
        ('add_to_cart', 'Add to Cart'),
        ('checkout', 'Checkout'),
        ('payment', 'Payment'),
        ('book_appointment', 'Book Appointment'),
        ('cancel_appointment', 'Cancel Appointment'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_details = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
    
    def __str__(self):
        user_identifier = self.user.username if self.user else self.session_id
        return f"{user_identifier} - {self.get_action_display()} at {self.timestamp}"
