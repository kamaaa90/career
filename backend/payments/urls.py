from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'coupons', views.CouponViewSet)
router.register(r'invoices', views.InvoiceViewSet)

urlpatterns = [
    # PayPal endpoints
    path('create-paypal-order/', views.CreatePayPalOrderView.as_view(), name='create-paypal-order'),
    path('capture-paypal-order/', views.CapturePayPalOrderView.as_view(), name='capture-paypal-order'),
    
    # Coupon validation
    path('validate-coupon/', views.ValidateCouponView.as_view(), name='validate-coupon'),
    
    # Order management
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order-confirmation/<uuid:order_id>/', views.OrderConfirmationView.as_view(), name='order-confirmation'),
    
    # User orders
    path('my-orders/', views.UserOrdersView.as_view(), name='my-orders'),
    path('my-invoices/', views.UserInvoicesView.as_view(), name='my-invoices'),
]

urlpatterns += router.urls
