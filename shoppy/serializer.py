from rest_framework import serializers
from .models import User, Product, Cart, Order, OrderItem, Invoice
from django.contrib.auth.hashers import make_password

# ----------------------  Auth ----------------------

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name', 'email', 'password', 'address', 'phone',
            'district', 'state', 'country', 'pincode'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LogoutSerializer(serializers.Serializer):
    email = serializers.EmailField()

# ----------------------  Product ----------------------

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductRestockSerializer(serializers.Serializer):
    name = serializers.CharField()
    brand = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

# ----------------------  Cart & Orders ----------------------

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

# ----------------------  Shipment ----------------------

class ShipmentStatusSerializer(serializers.Serializer):
    email = serializers.EmailField()
    order_id = serializers.IntegerField()
    shipment_status = serializers.ChoiceField(choices=[
        ('Pending', 'Pending'),
        ('Dispatched', 'Dispatched'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered')
    ])

# ----------------------  Direct Order ----------------------

class DirectOrderProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class DirectOrderSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    products = DirectOrderProductSerializer(many=True)
    confirm_dispatch = serializers.ChoiceField(choices=["yes", "no"])
    dispatch_address = serializers.CharField(required=False, allow_blank=True)
    dispatch_phone = serializers.CharField(required=False, allow_blank=True)
    payment_mode = serializers.ChoiceField(choices=["cod", "online"])
    distance = serializers.IntegerField()

    def validate(self, data):
        if data["confirm_dispatch"] == "no":
            if not data.get("dispatch_address") or not data.get("dispatch_phone"):
                raise serializers.ValidationError("Dispatch address and phone are required when confirm_dispatch is 'no'.")
        return data

# ----------------------  Admin ----------------------

class AdminDashboardSerializer(serializers.Serializer):
    email = serializers.EmailField()

