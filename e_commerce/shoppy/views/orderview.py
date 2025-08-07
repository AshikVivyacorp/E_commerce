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
    save_invoice_pdf_to_model
)


class CartView(APIView):
    @swagger_auto_schema(request_body=CartSerializer)
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product"].id
            user_id = serializer.validated_data["user"].id

            existing = Cart.objects.filter(product_id=product_id, user_id=user_id).first()
            if existing:
                return Response({"error": "Product already in cart"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.query_params.get("user_id")
        cart_items = Cart.objects.filter(user_id=user_id)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"user_id": openapi.Schema(type=openapi.TYPE_INTEGER)}
    ))
    def delete(self, request):
        user_id = request.data.get("user_id")
        Cart.objects.filter(user_id=user_id).delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)


class RemoveCartItemView(APIView):
    def delete(self, request, id):
        item = Cart.objects.filter(id=id).first()
        if not item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)


class PlaceCartOrderView(APIView):
    @swagger_auto_schema(request_body=DirectOrderSerializer)
    def post(self, request):
        serializer = DirectOrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.get(id=data["user_id"])
            cart_items = Cart.objects.filter(user=user)

            if not cart_items:
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            dispatch_address = data.get("dispatch_address") if data["confirm_dispatch"] == "no" else user.address
            dispatch_phone = data.get("dispatch_phone") if data["confirm_dispatch"] == "no" else user.phone

            if not dispatch_address or not dispatch_phone:
                return Response({
                    "error": "Dispatch address and phone are required. Either confirm_dispatch='no' and provide them, or ensure the user profile has both set."
                }, status=status.HTTP_400_BAD_REQUEST)

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

            pdf = generate_invoice_pdf(order, order.items.all(), total_amount, shipping_fee, data["payment_mode"], gst_amount, cod_surcharge)
            invoice = save_invoice_pdf_to_model(order, pdf)
            send_invoice_email(user.email, pdf, order.id)

            return Response({"message": "Order placed successfully", "order_id": order.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DirectOrderView(APIView):
    @swagger_auto_schema(request_body=DirectOrderSerializer)
    def post(self, request):
        serializer = DirectOrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.filter(id=data["user_id"]).first()
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            dispatch_address = data.get("dispatch_address") if data["confirm_dispatch"] == "no" else user.address
            dispatch_phone = data.get("dispatch_phone") if data["confirm_dispatch"] == "no" else user.phone

            if not dispatch_address or not dispatch_phone:
                return Response({
                    "error": "Dispatch address and phone are required. Either confirm_dispatch='no' and provide them, or ensure the user profile has both set."
                }, status=status.HTTP_400_BAD_REQUEST)

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
                    return Response({"error": f"Insufficient stock for product ID {item['product_id']}"},
                                    status=status.HTTP_400_BAD_REQUEST)

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

            pdf = generate_invoice_pdf(order, order.items.all(), total_amount, shipping_fee, data["payment_mode"], gst_amount, cod_surcharge)
            invoice = save_invoice_pdf_to_model(order, pdf)
            send_invoice_email(user.email, pdf, order.id)

            return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewInvoicePDF(APIView):
    def get(self, request, id):
        invoice = Invoice.objects.filter(order_id=id).first()
        if not invoice:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"pdf_url": invoice.pdf_file.url})


