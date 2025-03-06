from rest_framework import serializers
from django.contrib.auth.models import User
from services.serializers import ServiceSerializer, ServicePackageSerializer
from .models import TimeSlot, Appointment, AppointmentReminder, AvailabilityException


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for the TimeSlot model."""
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceSerializer.Meta.model.objects.all(),
        source='service',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = TimeSlot
        fields = [
            'id', 'day_of_week', 'start_time', 'end_time', 'service', 'service_id',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AppointmentReminderSerializer(serializers.ModelSerializer):
    """Serializer for the AppointmentReminder model."""
    
    class Meta:
        model = AppointmentReminder
        fields = [
            'id', 'appointment', 'reminder_type', 'reminder_time', 'is_sent',
            'sent_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_sent', 'sent_at', 'created_at', 'updated_at']


class AvailabilityExceptionSerializer(serializers.ModelSerializer):
    """Serializer for the AvailabilityException model."""
    
    class Meta:
        model = AvailabilityException
        fields = [
            'id', 'title', 'description', 'start_datetime', 'end_datetime',
            'is_recurring', 'recurrence_pattern', 'recurrence_end_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for the Appointment model."""
    user = UserBasicSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceSerializer.Meta.model.objects.all(),
        source='service',
        write_only=True,
        required=False,
        allow_null=True
    )
    package = ServicePackageSerializer(read_only=True)
    package_id = serializers.PrimaryKeyRelatedField(
        queryset=ServicePackageSerializer.Meta.model.objects.all(),
        source='package',
        write_only=True,
        required=False,
        allow_null=True
    )
    reminders = AppointmentReminderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'appointment_number', 'user', 'user_id', 'service', 'service_id',
            'package', 'package_id', 'date', 'start_time', 'end_time', 'status',
            'notes', 'location', 'meeting_link', 'reminders', 'created_at', 'updated_at'
        ]
        read_only_fields = ['appointment_number', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        """Validate that at least one of service or package is provided."""
        service = attrs.get('service')
        package = attrs.get('package')
        
        if not service and not package:
            raise serializers.ValidationError(
                "At least one of service or package must be provided."
            )
            
        return attrs


class AppointmentBookingSerializer(serializers.Serializer):
    """Serializer for booking appointments."""
    service_id = serializers.IntegerField(required=False, allow_null=True)
    package_id = serializers.IntegerField(required=False, allow_null=True)
    date = serializers.DateField(required=True)
    start_time = serializers.TimeField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate that at least one of service_id or package_id is provided."""
        service_id = attrs.get('service_id')
        package_id = attrs.get('package_id')
        
        if not service_id and not package_id:
            raise serializers.ValidationError(
                "At least one of service_id or package_id must be provided."
            )
            
        return attrs


class AppointmentRescheduleSerializer(serializers.Serializer):
    """Serializer for rescheduling appointments."""
    appointment_id = serializers.UUIDField(required=True)
    new_date = serializers.DateField(required=True)
    new_start_time = serializers.TimeField(required=True)


class AvailableSlotsSerializer(serializers.Serializer):
    """Serializer for available time slots."""
    date = serializers.DateField(required=False)
    service_id = serializers.IntegerField(required=False)
    package_id = serializers.IntegerField(required=False)
