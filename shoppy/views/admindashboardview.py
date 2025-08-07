<<<<<<< HEAD
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
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema

from shoppy.models import User, Product, Order
from shoppy.utils import is_admin, build_response, get_logger

_logger = get_logger()
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)


class AdminDashboardSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AdminDashboardView(APIView):
    @swagger_auto_schema(query_serializer=AdminDashboardSerializer)
    def get(self, request):
<<<<<<< HEAD
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

=======
        email = request.query_params.get("email")

        if not email or not is_admin(email):
            _logger.warning(f"Unauthorized dashboard access attempt by {email}")
            return Response(build_response(
                403, "Failed", "Access denied", statusFlag=False
            ), status=403)

        try:
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
            users_count = User.objects.count()
            products_count = Product.objects.count()
            orders_count = Order.objects.count()
            total_sales = sum(order.total for order in Order.objects.all())
<<<<<<< HEAD
            stats = {
=======

            dashboard_data = {
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
                "total_users": users_count,
                "total_products": products_count,
                "total_orders": orders_count,
                "total_sales": float(total_sales)
            }
<<<<<<< HEAD
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
=======

            _logger.info(f"Admin dashboard accessed by {email}")
            return Response(build_response(
                200, "Success", "Dashboard data fetched successfully", data=dashboard_data
            ), status=200)

        except Exception as e:
            _logger.error(f"Error fetching dashboard data: {str(e)}")
            return Response(build_response(
                500, "Failed", "Internal server error", errorDetails=str(e), statusFlag=False
            ), status=500)
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
