from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Notification, UserPreference, SavedService, SavedPackage

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

class UserPreferenceInline(admin.StackedInline):
    model = UserPreference
    can_delete = False
    verbose_name_plural = 'User Preferences'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, UserPreferenceInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')
    list_select_related = ('profile',)
    
    def get_phone(self, instance):
        return instance.profile.phone_number
    get_phone.short_description = 'Phone Number'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'user__email')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'notification_type', 'title', 'message', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

@admin.register(SavedService)
class SavedServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_name', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'service_name')
    readonly_fields = ('saved_at',)

@admin.register(SavedPackage)
class SavedPackageAdmin(admin.ModelAdmin):
    list_display = ('user', 'package_name', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'package_name')
    readonly_fields = ('saved_at',)
