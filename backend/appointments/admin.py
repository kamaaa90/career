from django.contrib import admin
from django.utils import timezone
from .models import TimeSlot, Appointment, AppointmentReminder, AvailabilityException

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('day_of_week', 'start_time', 'end_time')
    
    def get_day_display(self, obj):
        return obj.get_day_of_week_display()
    get_day_display.short_description = 'Day'
    get_day_display.admin_order_field = 'day_of_week'

class AppointmentReminderInline(admin.TabularInline):
    model = AppointmentReminder
    extra = 1
    fields = ('reminder_type', 'scheduled_time', 'status', 'sent_at')
    readonly_fields = ('sent_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'get_full_name', 'service', 'package', 'date', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'date', 'service', 'package')
    search_fields = ('appointment_id', 'first_name', 'last_name', 'email', 'phone', 'notes')
    readonly_fields = ('appointment_id', 'created_at', 'updated_at')
    inlines = [AppointmentReminderInline]
    date_hierarchy = 'date'
    actions = ['confirm_appointments', 'cancel_appointments', 'mark_as_completed', 'mark_as_no_show']
    fieldsets = (
        (None, {
            'fields': ('appointment_id', 'user', 'status')
        }),
        ('Service Information', {
            'fields': ('service', 'package')
        }),
        ('Schedule', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Client Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Client Name'
    
    def confirm_appointments(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} appointments have been confirmed.')
    confirm_appointments.short_description = "Mark selected appointments as confirmed"
    
    def cancel_appointments(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} appointments have been cancelled.')
    cancel_appointments.short_description = "Mark selected appointments as cancelled"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} appointments have been marked as completed.')
    mark_as_completed.short_description = "Mark selected appointments as completed"
    
    def mark_as_no_show(self, request, queryset):
        updated = queryset.update(status='no_show')
        self.message_user(request, f'{updated} appointments have been marked as no-show.')
    mark_as_no_show.short_description = "Mark selected appointments as no-show"

@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'reminder_type', 'scheduled_time', 'status', 'sent_at')
    list_filter = ('reminder_type', 'status', 'scheduled_time')
    search_fields = ('appointment__first_name', 'appointment__last_name', 'appointment__email')
    readonly_fields = ('created_at', 'sent_at')
    actions = ['mark_as_sent', 'mark_as_pending']
    fieldsets = (
        (None, {
            'fields': ('appointment', 'reminder_type')
        }),
        ('Scheduling', {
            'fields': ('scheduled_time', 'status', 'sent_at')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def mark_as_sent(self, request, queryset):
        updated = queryset.update(status='sent', sent_at=timezone.now())
        self.message_user(request, f'{updated} reminders have been marked as sent.')
    mark_as_sent.short_description = "Mark selected reminders as sent"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending', sent_at=None)
        self.message_user(request, f'{updated} reminders have been marked as pending.')
    mark_as_pending.short_description = "Mark selected reminders as pending"

@admin.register(AvailabilityException)
class AvailabilityExceptionAdmin(admin.ModelAdmin):
    list_display = ('description', 'exception_type', 'start_datetime', 'end_datetime', 'created_at')
    list_filter = ('exception_type', 'start_datetime')
    search_fields = ('description',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('description', 'exception_type')
        }),
        ('Time Period', {
            'fields': ('start_datetime', 'end_datetime')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
