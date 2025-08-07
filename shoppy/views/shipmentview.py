import logging
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from shoppy.models import Order
from shoppy.serializer import ShipmentStatusSerializer
from shoppy.utils import is_admin

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class ShipmentStatusUpdateView(APIView):
    @swagger_auto_schema(request_body=ShipmentStatusSerializer)
    def post(self, request):
        try:
            serializer = ShipmentStatusSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                order_id = serializer.validated_data['order_id']
                shipment_status = serializer.validated_data['shipment_status']

                if not is_admin(email):
                    data = {
                        'response_code': 403,
                        'status': 'Failed',
                        'message': 'Access denied',
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"Non-admin attempted to update shipment status: {email}")
                    return Response(data, status=status.HTTP_403_FORBIDDEN)

                order = Order.objects.filter(id=order_id).first()
                if not order:
                    data = {
                        'response_code': 404,
                        'status': 'Failed',
                        'message': 'Order not found',
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"Order not found on shipment status update: {order_id}")
                    return Response(data, status=status.HTTP_404_NOT_FOUND)

                order.shipment_status = shipment_status
                order.save()
                data = {
                    'response_code': 200,
                    'status': 'Success',
                    'message': 'Shipment status updated',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': {}
                }
                logger.info(f"Shipment status updated to {shipment_status} for order {order_id}")
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid shipment status data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning("Invalid shipment status data on update")
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                'response_code': 500,
                'status': 'Failed',
                'message': 'Internal server error',
                'statusFlag': False,
                'errorDetails': str(e),
                'data': {}
            }
            logger.error("Internal server error in ShipmentStatusUpdateView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
