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
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
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

