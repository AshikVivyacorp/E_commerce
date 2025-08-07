from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from shoppy.models import User, Product, Order
from shoppy.utils import is_admin


class AdminDashboardSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AdminDashboardView(APIView):
    @swagger_auto_schema(query_serializer=AdminDashboardSerializer)
    def get(self, request):
        email = request.query_params.get("email")
        if not email or not is_admin(email):
            return Response({"detail": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        users_count = User.objects.count()
        products_count = Product.objects.count()
        orders_count = Order.objects.count()
        total_sales = sum(order.total for order in Order.objects.all())

        return Response({
            "total_users": users_count,
            "total_products": products_count,
            "total_orders": orders_count,
            "total_sales": float(total_sales)
        })
