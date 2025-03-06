from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'time-slots', views.TimeSlotViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'availability-exceptions', views.AvailabilityExceptionViewSet)

urlpatterns = [
    # Availability endpoints
    path('available-slots/', views.AvailableSlotsView.as_view(), name='available-slots'),
    path('available-slots/<str:date>/', views.AvailableSlotsForDateView.as_view(), name='available-slots-for-date'),
    
    # Booking endpoints
    path('book-appointment/', views.BookAppointmentView.as_view(), name='book-appointment'),
    path('reschedule-appointment/<uuid:appointment_id>/', views.RescheduleAppointmentView.as_view(), name='reschedule-appointment'),
    path('cancel-appointment/<uuid:appointment_id>/', views.CancelAppointmentView.as_view(), name='cancel-appointment'),
    
    # User appointments
    path('my-appointments/', views.UserAppointmentsView.as_view(), name='my-appointments'),
    path('appointment-details/<uuid:appointment_id>/', views.AppointmentDetailsView.as_view(), name='appointment-details'),
]

urlpatterns += router.urls
