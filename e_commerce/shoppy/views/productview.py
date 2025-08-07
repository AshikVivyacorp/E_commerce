from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from knox.auth import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from shoppy.models import Product
from shoppy.serializer import ProductSerializer, ProductRestockSerializer
from shoppy.utils import notify_admin_out_of_stock, notify_users_product_restocked


# ----------------- Custom Admin Permission ------------------

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, 'is_admin', False)
        )


# ----------------- Product Views ------------------

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, id):
        product = Product.objects.filter(id=id).first()
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id):
        product = Product.objects.filter(id=id).first()
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)


class ProductRestockView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductRestockSerializer)
    def post(self, request, id):
        product = Product.objects.filter(id=id).first()
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        if quantity:
            product.quantity += int(quantity)
            product.save()
            notify_users_product_restocked(product)
            return Response({"message": "Product restocked"}, status=status.HTTP_200_OK)

        return Response({"error": "Quantity required"}, status=status.HTTP_400_BAD_REQUEST)
