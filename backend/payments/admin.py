from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Payment, Coupon, Invoice

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('item_type', 'service', 'package', 'quantity', 'price', 'discount', 'total_price')
    readonly_fields = ('total_price',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ('payment_id', 'amount', 'payment_method', 'status', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'email', 'get_full_name', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'email', 'first_name', 'last_name', 'user__username', 'user__email')
    readonly_fields = ('order_id', 'created_at', 'updated_at', 'ip_address', 'user_agent')
    inlines = [OrderItemInline, PaymentInline]
    fieldsets = (
        (None, {
            'fields': ('order_id', 'user', 'status')
        }),
        ('Customer Information', {
            'fields': ('email', 'first_name', 'last_name', 'phone')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'notes')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Customer Name'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order_link', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'order__order_id', 'order__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('order', 'payment_id', 'amount', 'payment_method', 'status')
        }),
        ('Transaction Data', {
            'fields': ('transaction_data',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def order_link(self, obj):
        url = f"/admin/payments/order/{obj.order.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.order.order_id)
    order_link.short_description = 'Order'

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'max_uses', 'current_uses', 'is_active', 'is_valid')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code', 'description')
    readonly_fields = ('created_at', 'is_valid')
    fieldsets = (
        (None, {
            'fields': ('code', 'discount_type', 'discount_value', 'description')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_to', 'is_active', 'is_valid')
        }),
        ('Usage', {
            'fields': ('max_uses', 'current_uses')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order_link', 'status', 'issue_date', 'due_date', 'created_at')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'order__order_id', 'order__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('order', 'invoice_number', 'status')
        }),
        ('Dates', {
            'fields': ('issue_date', 'due_date')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def order_link(self, obj):
        url = f"/admin/payments/order/{obj.order.id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.order.order_id)
    order_link.short_description = 'Order'
