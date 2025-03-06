from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'preferences', views.UserPreferenceViewSet)
router.register(r'saved-services', views.SavedServiceViewSet)
router.register(r'saved-packages', views.SavedPackageViewSet)

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    
    # Profile management
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('me/profile/', views.CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('me/preferences/', views.CurrentUserPreferencesView.as_view(), name='current-user-preferences'),
    
    # Notifications
    path('me/notifications/', views.UserNotificationsView.as_view(), name='user-notifications'),
    path('me/notifications/mark-read/<int:notification_id>/', views.MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('me/notifications/mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-notifications-read'),
    
    # Saved items
    path('me/saved-services/', views.UserSavedServicesView.as_view(), name='user-saved-services'),
    path('me/saved-packages/', views.UserSavedPackagesView.as_view(), name='user-saved-packages'),
]

urlpatterns += router.urls
