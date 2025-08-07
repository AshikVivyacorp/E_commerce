<<<<<<< HEAD
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
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from shoppy.models import Product, Cart, Order, OrderItem, Invoice, User
from shoppy.serializer import (
    CartSerializer, DirectOrderSerializer, OrderSerializer, OrderItemSerializer, InvoiceSerializer
)
from shoppy.utils import (
    generate_invoice_pdf,
    send_invoice_email,
    calculate_cart_total,
    is_admin,
    create_user_session,
    save_invoice_pdf_to_model,
    build_response,
    get_logger
)

_logger=get_logger()


class CartView(APIView):
    @swagger_auto_schema(request_body=CartSerializer)
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product"].id
            user_id = serializer.validated_data["user"].id

            existing = Cart.objects.filter(product_id=product_id, user_id=user_id).first()
            if existing:
                _logger.warning("Product already in cart")
                return Response(build_response(400, "Failed", "Product already in cart", statusFlag=False), status=400)

            serializer.save()
            _logger.info("Product added to cart")
            return Response(build_response(201, "Success", "Product added to cart", data=serializer.data), status=201)

        _logger.error("Invalid cart data: %s", serializer.errors)
        return Response(build_response(400, "Failed", "Invalid data", data=serializer.errors, statusFlag=False),
                        status=400)

    def get(self, request):
        user_id = request.query_params.get("user_id")
        cart_items = Cart.objects.filter(user_id=user_id)
        serializer = CartSerializer(cart_items, many=True)
        return Response(build_response(200, "Success", "Cart items fetched", data=serializer.data))

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"user_id": openapi.Schema(type=openapi.TYPE_INTEGER)}
    ))
    def delete(self, request):
        user_id = request.data.get("user_id")
        Cart.objects.filter(user_id=user_id).delete()
        _logger.info(f"Cart cleared for user {user_id}")
        return Response(build_response(204, "Success", "Cart cleared"))


class RemoveCartItemView(APIView):
    def delete(self, request, id):
        item = Cart.objects.filter(id=id).first()
        if not item:
            _logger.warning("Cart item not found")
            return Response(build_response(404, "Failed", "Item not found", statusFlag=False), status=404)
        item.delete()
        _logger.info(f"Cart item {id} removed")
        return Response(build_response(204, "Success", "Item removed from cart"))


class PlaceCartOrderView(APIView):
    @swagger_auto_schema(request_body=DirectOrderSerializer)
    def post(self, request):
        serializer = DirectOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                user = User.objects.get(id=data["user_id"])
                cart_items = Cart.objects.filter(user=user)

                if not cart_items:
                    return Response(build_response(400, "Failed", "Cart is empty", statusFlag=False), status=400)

                dispatch_address = data.get("dispatch_address") if data["confirm_dispatch"] == "no" else user.address
                dispatch_phone = data.get("dispatch_phone") if data["confirm_dispatch"] == "no" else user.phone

                if not dispatch_address or not dispatch_phone:
                    return Response(build_response(
                        400, "Failed",
                        "Dispatch address and phone required",
                        statusFlag=False
                    ), status=400)

                order = Order.objects.create(
                    user=user,
                    dispatch_address=dispatch_address,
                    dispatch_phone=dispatch_phone,
                    payment_mode=data["payment_mode"],
                    distance=data["distance"],
                    is_direct=False
                )

                total_amount = 0
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        brand=item.product.brand,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                    item.product.quantity -= item.quantity
                    item.product.sold_count += item.quantity
                    item.product.save()
                    total_amount += item.product.price * item.quantity

                cart_items.delete()

                shipping_fee = 50
                cod_surcharge = data["distance"] * 10 if data["payment_mode"].lower() == "cod" else 0
                gst_amount = total_amount * 0.08 if data["payment_mode"].lower() == "online" else 0
                total = total_amount + shipping_fee + cod_surcharge + gst_amount

                order.total = total
                order.save()

                pdf = generate_invoice_pdf(order, order.items.all(), total_amount, shipping_fee, data["payment_mode"],
                                           gst_amount, cod_surcharge)
                invoice = save_invoice_pdf_to_model(order, pdf)
                send_invoice_email(user.email, pdf, order.id)

                return Response(build_response(200, "Success", "Order placed", data={"order_id": order.id}))
            except Exception as e:
                _logger.error("Error placing cart order: %s", str(e))
                return Response(
                    build_response(500, "Failed", "Internal server error", errorDetails=str(e), statusFlag=False),
                    status=500)

        return Response(build_response(400, "Failed", "Invalid data", data=serializer.errors, statusFlag=False),
                        status=400)


class DirectOrderView(APIView):
    @swagger_auto_schema(request_body=DirectOrderSerializer)
    def post(self, request):
        serializer = DirectOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                user = User.objects.filter(id=data["user_id"]).first()
                if not user:
                    return Response(build_response(404, "Failed", "User not found", statusFlag=False), status=404)

                dispatch_address = data.get("dispatch_address") if data["confirm_dispatch"] == "no" else user.address
                dispatch_phone = data.get("dispatch_phone") if data["confirm_dispatch"] == "no" else user.phone

                if not dispatch_address or not dispatch_phone:
                    return Response(build_response(
                        400, "Failed",
                        "Dispatch address and phone required",
                        statusFlag=False
                    ), status=400)

                order = Order.objects.create(
                    user=user,
                    dispatch_address=dispatch_address,
                    dispatch_phone=dispatch_phone,
                    payment_mode=data["payment_mode"],
                    distance=data.get("distance", 0),
                    is_direct=True
                )

                total_amount = 0
                for item in data["products"]:
                    product = Product.objects.filter(id=item["product_id"]).first()
                    if not product or product.quantity < item["quantity"]:
                        return Response(build_response(
                            400, "Failed",
                            f"Insufficient stock for product ID {item['product_id']}",
                            statusFlag=False
                        ), status=400)

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        brand=product.brand,
                        quantity=item["quantity"],
                        price=product.price
                    )
                    product.quantity -= item["quantity"]
                    product.sold_count += item["quantity"]
                    product.save()
                    total_amount += product.price * item["quantity"]

                shipping_fee = 50
                cod_surcharge = data["distance"] * 10 if data["payment_mode"].lower() == "cod" else 0
                gst_amount = total_amount * 0.08 if data["payment_mode"].lower() == "online" else 0
                total = total_amount + shipping_fee + cod_surcharge + gst_amount

                order.total = total
                order.save()

                pdf = generate_invoice_pdf(order, order.items.all(), total_amount, shipping_fee, data["payment_mode"],
                                           gst_amount, cod_surcharge)
                invoice = save_invoice_pdf_to_model(order, pdf)
                send_invoice_email(user.email, pdf, order.id)

                return Response(build_response(201, "Success", "Order placed", data={"order_id": order.id}), status=201)
            except Exception as e:
                _logger.error("Error placing direct order: %s", str(e))
                return Response(
                    build_response(500, "Failed", "Internal server error", errorDetails=str(e), statusFlag=False),
                    status=500)

        return Response(build_response(400, "Failed", "Invalid data", data=serializer.errors, statusFlag=False),
                        status=400)


class ViewInvoicePDFView(APIView):


    def get(self, request, order_id):
        try:
            invoice = Invoice.objects.filter(order_id=order_id).first()
            if not invoice:
                _logger.warning(f"Invoice not found for order {order_id}")
                return Response({
                    "response_code": 404,
                    "status": "Failed",
                    "message": "Invoice not found",
                    "statusFlag": False,
                    "errorDetails": None,
                    "data": {}
                }, status=status.HTTP_404_NOT_FOUND)

            _logger.info(f"Invoice fetched for order {order_id}")
            return Response({
                "response_code": 200,
                "status": "Success",
                "message": "Invoice URL fetched",
                "statusFlag": True,
                "errorDetails": None,
                "data": {"pdf_url": invoice.pdf_file.url}
            }, status=status.HTTP_200_OK)
        except Exception as e:
            _logger.error(f"Error fetching invoice for order {order_id}: {str(e)}", exc_info=True)
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
            return Response({
                "response_code": 500,
                "status": "Failed",
                "message": "Internal server error",
                "statusFlag": False,
                "errorDetails": str(e),
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
