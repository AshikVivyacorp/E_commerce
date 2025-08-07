from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from shoppy.models import Order
from shoppy.serializer import ShipmentStatusSerializer
from shoppy.utils import is_admin


class ShipmentStatusUpdateView(APIView):
    @swagger_auto_schema(request_body=ShipmentStatusSerializer)
    def post(self, request):
        serializer = ShipmentStatusSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            order_id = serializer.validated_data['order_id']
            shipment_status = serializer.validated_data['shipment_status']

            if not is_admin(email):
                return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

            order = Order.objects.filter(id=order_id).first()
            if not order:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

            order.shipment_status = shipment_status
            order.save()
            return Response({"message": "Shipment status updated"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
