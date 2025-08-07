import logging
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from shoppy.models import User, Product, Order
from shoppy.utils import is_admin

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


class AdminDashboardSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AdminDashboardView(APIView):
    @swagger_auto_schema(query_serializer=AdminDashboardSerializer)
    def get(self, request):
        try:
            email = request.query_params.get("email")
            if not email or not is_admin(email):
                data = {
                    'response_code': 403,
                    'status': 'Failed',
                    'message': 'Access denied',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Admin dashboard access denied for email: {email}")
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            users_count = User.objects.count()
            products_count = Product.objects.count()
            orders_count = Order.objects.count()
            total_sales = sum(order.total for order in Order.objects.all())
            stats = {
                "total_users": users_count,
                "total_products": products_count,
                "total_orders": orders_count,
                "total_sales": float(total_sales)
            }
            logger.info(f"Admin dashboard stats fetched for: {email}")
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'Dashboard stats fetched',
                'statusFlag': True,
                'errorDetails': None,
                'data': stats
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                'response_code': 500,
                'status': 'Failed',
                'message': 'Internal server error',
                'statusFlag': False,
                'errorDetails': str(e),
                'data': {}
            }
            logger.error("Internal server error in AdminDashboardView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
