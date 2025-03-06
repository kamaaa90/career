from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.ServiceCategoryViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'packages', views.ServicePackageViewSet)
router.register(r'testimonials', views.TestimonialViewSet)

urlpatterns = [
    # Custom endpoints
    path('featured-services/', views.FeaturedServicesView.as_view(), name='featured-services'),
    path('featured-packages/', views.FeaturedPackagesView.as_view(), name='featured-packages'),
    path('featured-testimonials/', views.FeaturedTestimonialsView.as_view(), name='featured-testimonials'),
]

urlpatterns += router.urls
