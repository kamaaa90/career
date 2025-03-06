from rest_framework import serializers
from django.contrib.auth.models import User
from services.serializers import ServiceSerializer, ServicePackageSerializer
from .models import Order, OrderItem, Payment, Coupon, Invoice


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CouponSerializer(serializers.ModelSerializer):
    """Serializer for the Coupon model."""
    
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'discount_type', 'discount_value', 'minimum_order_amount',
            'is_active', 'valid_from', 'valid_to', 'usage_limit', 'times_used',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['times_used', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model."""
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
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'service', 'service_id', 'package', 'package_id',
            'quantity', 'unit_price', 'total_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['order', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        """Validate that at least one of service or package is provided."""
        service = attrs.get('service')
        package = attrs.get('package')
        
        if not service and not package:
            raise serializers.ValidationError(
                "At least one of service or package must be provided."
            )
            
        return attrs


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for the Payment model."""
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'payment_method', 'transaction_id', 'amount', 'status',
            'payment_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for the Invoice model."""
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'order', 'invoice_number', 'invoice_date', 'due_date',
            'billing_address', 'billing_email', 'billing_phone', 'subtotal',
            'tax_amount', 'discount_amount', 'total_amount', 'notes', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['invoice_number', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model."""
    user = UserBasicSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    coupon = CouponSerializer(read_only=True)
    coupon_code = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_id', 'status', 'items', 'subtotal',
            'tax_amount', 'discount_amount', 'total_amount', 'coupon', 'coupon_code',
            'notes', 'shipping_address', 'billing_address', 'payments', 'invoice',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'subtotal', 'tax_amount', 'discount_amount', 
                           'total_amount', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create an order with items."""
        coupon_code = validated_data.pop('coupon_code', None)
        items_data = self.context.get('items', [])
        
        # Try to get coupon if code provided
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            except Coupon.DoesNotExist:
                pass
        
        # Create order
        order = Order.objects.create(
            user=validated_data['user'],
            status=validated_data.get('status', 'pending'),
            notes=validated_data.get('notes', ''),
            shipping_address=validated_data.get('shipping_address', ''),
            billing_address=validated_data.get('billing_address', ''),
            coupon=coupon
        )
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                service=item_data.get('service'),
                package=item_data.get('package'),
                quantity=item_data.get('quantity', 1),
                unit_price=item_data.get('unit_price'),
                total_price=item_data.get('total_price')
            )
        
        # Calculate order totals
        order.calculate_totals()
        
        return order


class PayPalOrderSerializer(serializers.Serializer):
    """Serializer for creating PayPal orders."""
    order_id = serializers.UUIDField(required=True)


class CouponValidationSerializer(serializers.Serializer):
    """Serializer for coupon validation."""
    code = serializers.CharField(required=True)
    order_total = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
