"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

# Customize admin site
admin.site.site_header = 'Career Services Administration'
admin.site.site_title = 'Career Services Admin Portal'
admin.site.index_title = 'Welcome to Career Services Admin Portal'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', include_docs_urls(title='Career Services API')),
    
    # REST Framework browsable API
    path('api-auth/', include('rest_framework.urls')),
    
    # CKEditor URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # App URLs
    path('api/services/', include('services.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/users/', include('users.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
