<<<<<<< HEAD
import logging
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from shoppy.models import Product
from shoppy.serializer import ProductSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'List of products',
                'statusFlag': True,
                'errorDetails': None,
                'data': serializer.data
            }
            logger.info("Product list fetched")
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
            logger.error("Internal server error in ProductListView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductCreateView(APIView):
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from knox.auth import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from shoppy.models import Product
from shoppy.serializer import ProductSerializer, ProductRestockSerializer
from shoppy.utils import (
    notify_admin_out_of_stock,
    notify_users_product_restocked,
    get_logger,
    build_response
)

_logger = get_logger()


# ----------------- Custom Admin Permission ------------------

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, 'is_admin', False)
        )


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
        _logger.info("Fetched all product list")
        return Response(build_response(200, "Success", "Product list fetched", data=serializer.data))


class ProductCreateView(APIView):
    authentication_classes = [TokenAuthentication]
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
<<<<<<< HEAD
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save()
                data = {
                    'response_code': 201,
                    'status': 'Success',
                    'message': 'Product created',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': serializer.data
                }
                logger.info(f"Product created: {product.name}")
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid product data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning("Invalid product data on creation")
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
            logger.error("Internal server error in ProductCreateView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            product = self.get_object(pk)
            if product is None:
                data = {
                    'response_code': 404,
                    'status': 'Failed',
                    'message': 'Product not found',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Product not found: {pk}")
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'Product details',
                'statusFlag': True,
                'errorDetails': None,
                'data': serializer.data
            }
            logger.info(f"Product details fetched: {pk}")
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
            logger.error("Internal server error in ProductDetailView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        try:
            product = self.get_object(pk)
            if product is None:
                data = {
                    'response_code': 404,
                    'status': 'Failed',
                    'message': 'Product not found',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Product not found on update: {pk}")
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'response_code': 200,
                    'status': 'Success',
                    'message': 'Product updated',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': serializer.data
                }
                logger.info(f"Product updated: {pk}")
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid product data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning(f"Invalid product data on update: {pk}")
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
            logger.error("Internal server error in ProductUpdateView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def delete(self, request, pk):
        try:
            product = self.get_object(pk)
            if product is None:
                data = {
                    'response_code': 404,
                    'status': 'Failed',
                    'message': 'Product not found',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Product not found on delete: {pk}")
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            data = {
                'response_code': 200,
                'status': 'Success',
                'message': 'Product deleted',
                'statusFlag': True,
                'errorDetails': None,
                'data': {'id': pk}
            }
            logger.info(f"Product deleted: {pk}")
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
            logger.error("Internal server error in ProductDeleteView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductRestockView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            quantity = request.data.get("quantity", 0)
            product.stock += int(quantity)
            product.save()
            return Response({
                "response_code": 200,
                "status": "Success",
                "message": "Product restocked",
                "statusFlag": True,
                "errorDetails": None,
                "data": {
                    "product_id": product.id,
                    "new_stock": product.stock
                }
            }, status=200)
        except Product.DoesNotExist:
            return Response({
                "response_code": 400,
                "status": "Failed",
                "message": "Product not found",
                "statusFlag": False,
                "errorDetails": None,
                "data": {}
            }, status=400)
        except Exception as e:
            return Response({
                "response_code": 500,
                "status": "Failed",
                "message": "Internal server error",
                "statusFlag": False,
                "errorDetails": str(e),
                "data": {}
            }, status=500)

=======
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            _logger.info("Product created successfully")
            return Response(build_response(201, "Success", "Product created"), status=201)
        _logger.error(f"Product creation failed: {serializer.errors}")
        return Response(build_response(400, "Failed", "Invalid data", data=serializer.errors, statusFlag=False), status=400)


class ProductUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, id):
        product = Product.objects.filter(id=id).first()
        if not product:
            _logger.warning(f"Product with ID {id} not found for update")
            return Response(build_response(404, "Failed", "Product not found", statusFlag=False), status=404)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            _logger.info(f"Product {id} updated")
            return Response(build_response(200, "Success", "Product updated"))
        _logger.error(f"Product update failed: {serializer.errors}")
        return Response(build_response(400, "Failed", "Invalid data", data=serializer.errors, statusFlag=False), status=400)


class ProductDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id):
        product = Product.objects.filter(id=id).first()
        if not product:
            _logger.warning(f"Product with ID {id} not found for deletion")
            return Response(build_response(404, "Failed", "Product not found", statusFlag=False), status=404)

        product.delete()
        _logger.info(f"Product {id} deleted")
        return Response(build_response(204, "Success", "Product deleted"), status=204)


class ProductRestockView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductRestockSerializer)
    def post(self, request, id):
        product = Product.objects.filter(id=id).first()
        if not product:
            _logger.warning(f"Product with ID {id} not found for restock")
            return Response(build_response(
                404, "Failed", "Product not found", statusFlag=False
            ), status=404)

        quantity = request.data.get("quantity")
        if quantity:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than 0")
            except ValueError:
                _logger.warning("Invalid quantity provided for restock")
                return Response(build_response(
                    400, "Failed", "Invalid quantity", statusFlag=False
                ), status=400)

            product.quantity += quantity
            product.save()

            notify_users_product_restocked(product)
            _logger.info(f"Product {id} restocked with quantity {quantity}")

            return Response(build_response(
                200, "Success", "Product restocked"
            ), status=200)

        _logger.warning("Restock failed due to missing quantity")
        return Response(build_response(
            400, "Failed", "Quantity is required", statusFlag=False
        ), status=400)
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
