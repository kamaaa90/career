from django.contrib import admin
from .models import ServiceCategory, Service, ServicePackage, PackageService, ServiceFeature, PackageFeature, Testimonial

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'icon', 'order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ('name', 'description', 'is_highlighted', 'order')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discounted_price', 'level', 'is_featured', 'is_active')
    list_filter = ('category', 'level', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ServiceFeatureInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'level')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discounted_price')
        }),
        ('Display', {
            'fields': ('image', 'duration', 'is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class PackageServiceInline(admin.TabularInline):
    model = PackageService
    extra = 1
    fields = ('service', 'order')

class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 1
    fields = ('name', 'description', 'is_highlighted', 'order')

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_type', 'price', 'discounted_price', 'is_featured', 'is_active')
    list_filter = ('package_type', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PackageServiceInline, PackageFeatureInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'package_type')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discounted_price')
        }),
        ('Display', {
            'fields': ('image', 'is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'rating', 'service', 'package', 'is_featured')
    list_filter = ('rating', 'is_featured', 'created_at')
    search_fields = ('name', 'position', 'company', 'content')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'position', 'company', 'image', 'content', 'rating')
        }),
        ('Association', {
            'fields': ('service', 'package')
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
