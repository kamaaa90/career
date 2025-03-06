from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'analytics', views.AnalyticsViewSet)
router.register(r'page-visits', views.PageVisitViewSet)
router.register(r'financial-reports', views.FinancialReportViewSet)
router.register(r'service-performance', views.ServicePerformanceViewSet)
router.register(r'package-performance', views.PackagePerformanceViewSet)
router.register(r'user-activity', views.UserActivityViewSet)

urlpatterns = [
    # Dashboard overview
    path('overview/', views.DashboardOverviewView.as_view(), name='dashboard-overview'),
    
    # Analytics endpoints
    path('analytics/summary/', views.AnalyticsSummaryView.as_view(), name='analytics-summary'),
    path('analytics/period/<str:period_type>/', views.AnalyticsByPeriodView.as_view(), name='analytics-by-period'),
    
    # Financial endpoints
    path('financial/summary/', views.FinancialSummaryView.as_view(), name='financial-summary'),
    path('financial/period/<str:period_type>/', views.FinancialByPeriodView.as_view(), name='financial-by-period'),
    
    # Performance endpoints
    path('top-services/', views.TopServicesView.as_view(), name='top-services'),
    path('top-packages/', views.TopPackagesView.as_view(), name='top-packages'),
    
    # User activity
    path('recent-activity/', views.RecentActivityView.as_view(), name='recent-activity'),
]

urlpatterns += router.urls
