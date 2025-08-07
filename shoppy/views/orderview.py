import logging
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from shoppy.models import Order, Cart
from shoppy.serializer import OrderSerializer, CartSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CartSerializer)
    def post(self, request):
        try:
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                user_id = serializer.validated_data["user"].id
                product_id = serializer.validated_data["product"].id
                existing = Cart.objects.filter(user_id=user_id, product_id=product_id).first()
                if existing:
                    data = {
                        'response_code': 400,
                        'status': 'Failed',
                        'message': 'Product already in cart',
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"Cart item already exists for user {user_id}, product {product_id}")
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                data = {
                    'response_code': 201,
                    'status': 'Success',
                    'message': 'Product added to cart',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': serializer.data
                }
                logger.info(f"Product {product_id} added to cart for user {user_id}")
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid cart data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning("Invalid cart data on cart add")
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
            logger.error("Internal server error in CartView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            carts = Cart.objects.filter(user=request.user)
            serializer = CartSerializer(carts, many=True)
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'List of cart items',
                'statusFlag': True,
                'errorDetails': None,
                'data': serializer.data
            }
            logger.info(f"Cart items listed for user {request.user.id}")
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
            logger.error("Internal server error in CartListView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Cart.objects.get(pk=pk, user=user)
        except Cart.DoesNotExist:
            return None

    def delete(self, request, pk):
        try:
            cart = self.get_object(pk, request.user)
            if cart is None:
                data = {
                    'response_code': 404,
                    'status': 'Failed',
                    'message': 'Cart item not found',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Cart item not found for deletion: {pk}, user {request.user.id}")
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            cart.delete()
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'Cart item deleted',
                'statusFlag': True,
                'errorDetails': None,
                'data': {'id': pk}
            }
            logger.info(f"Cart item {pk} deleted for user {request.user.id}")
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
            logger.error("Internal server error in CartDeleteView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            carts = Cart.objects.filter(user=request.user)
            if not carts:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Cart is empty',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Place order failed: Cart is empty for user {request.user.id}")
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            # Business logic: convert cart items into an order, clear the cart
            # (You would need to replace this with your actual order creation logic)
            carts.delete()
            data = {
                'response_code': 201,
                'status': 'Success',
                'message': 'Order placed',
                'statusFlag': True,
                'errorDetails': None,
                'data': {}
            }
            logger.info(f"Order placed for user {request.user.id}")
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                'response_code': 500,
                'status': 'Failed',
                'message': 'Internal server error',
                'statusFlag': False,
                'errorDetails': str(e),
                'data': {}
            }
            logger.error("Internal server error in PlaceOrderView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            orders = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(orders, many=True)
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'List of orders',
                'statusFlag': True,
                'errorDetails': None,
                'data': serializer.data
            }
            logger.info(f"Orders listed for user {request.user.id}")
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
            logger.error("Internal server error in OrderListView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            order = self.get_object(pk, request.user)
            if order is None:
                data = {
                    'response_code': 404,
                    'status': 'Failed',
                    'message': 'Order not found',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Order not found: {pk}, user {request.user.id}")
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order)
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'Order details',
                'statusFlag': True,
                'errorDetails': None,
                'data': serializer.data
            }
            logger.info(f"Order details fetched: {pk}, user {request.user.id}")
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
            logger.error("Internal server error in OrderDetailView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaceCartOrderView(APIView):
    def post(self, request):
        try:
            # Simulate placing order (replace with real logic)
            return Response({
                "response_code": 200,
                "status": "Success",
                "message": "Order placed successfully",
                "statusFlag": True,
                "errorDetails": None,
                "data": {}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "response_code": 500,
                "status": "Failed",
                "message": "Internal server error",
                "statusFlag": False,
                "errorDetails": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DirectOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # This is a placeholder. You should replace it with actual logic
            return Response({
                "response_code": 200,
                "status": "Success",
                "message": "Direct order placed successfully",
                "statusFlag": True,
                "errorDetails": None,
                "data": {}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "response_code": 500,
                "status": "Failed",
                "message": "Internal server error",
                "statusFlag": False,
                "errorDetails": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
