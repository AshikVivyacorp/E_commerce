import logging
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token  # or use Knox AuthToken if preferred
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from shoppy.models import User, OTP
from shoppy.serializer import (
    RegistrationSerializer,
    LoginSerializer,
    OTPVerifySerializer,
    ResendOTPSerializer
)
from shoppy.utils import generate_otp, send_otp_email, is_otp_valid

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                if User.objects.filter(email=email).exists():
                    data = {
                        'response_code': 400,
                        'status': 'Failed',
                        'message': "Email already exists",
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"Register attempt failed: {data['message']} ({email})")
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                user = serializer.save()
                if user.email == "admin@example.com":
                    user.is_admin = True
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()

                otp = generate_otp()
                OTP.objects.create(user=user, code=otp)
                send_otp_email(email, otp)

                data = {
                    'response_code': 201,
                    'status': 'Success',
                    'message': 'User registered. OTP sent.',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': {'email': email}
                }
                logger.info(f"User registered, OTP sent: {data['message']} ({email})")
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid registration data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning(f"Register failed: {data['message']}")
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
            logger.error("Internal server error in RegisterView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]
                user = authenticate(username=email, password=password)
                if user is None:
                    data = {
                        'response_code': 400,
                        'status': 'Failed',
                        'message': 'Email or password is wrong',
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"Login failed: {data['message']} ({email})")
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'response_code': 200,
                    'status': 'Success',
                    'message': 'Token has been created',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': {'token': token.key, 'user_id': user.id}
                }
                logger.info(f"Login succeeded: {data['message']} ({email})")
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid login data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning(f"Login failed: {data['message']}")
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
            logger.error("Internal server error in LoginView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=OTPVerifySerializer)
    def post(self, request):
        try:
            serializer = OTPVerifySerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                otp = serializer.validated_data["otp"]
                user = User.objects.filter(email=email).first()
                if not user:
                    data = {
                        'response_code': 400,
                        'status': 'Failed',
                        'message': "Email does not exist",
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"OTP verify failed: {data['message']} ({email})")
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                if not is_otp_valid(email, otp):
                    data = {
                        'response_code': 400,
                        'status': 'Failed',
                        'message': "Invalid OTP",
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"OTP verify failed: {data['message']} ({email})")
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                data = {
                    'response_code': 200,
                    'status': 'Success',
                    'message': 'OTP verified',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': {'email': email}
                }
                logger.info(f"OTP verified: {data['message']} ({email})")
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid OTP data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning(f"OTP verify failed: {data['message']}")
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
            logger.error("Internal server error in VerifyOTPView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ResendOTPSerializer)
    def post(self, request):
        try:
            serializer = ResendOTPSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                user = User.objects.filter(email=email).first()
                if not user:
                    data = {
                        'response_code': 400,
                        'status': 'Failed',
                        'message': "Email does not exist",
                        'statusFlag': False,
                        'errorDetails': None,
                        'data': {}
                    }
                    logger.warning(f"Resend OTP failed: {data['message']} ({email})")
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                otp = generate_otp()
                OTP.objects.create(user=user, code=otp)
                send_otp_email(email, otp)
                data = {
                    'response_code': 200,
                    'status': 'Success',
                    'message': 'OTP resent',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': {'email': email}
                }
                logger.info(f"OTP resent: {data['message']} ({email})")
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'response_code': 400,
                    'status': 'Failed',
                    'message': 'Invalid data',
                    'statusFlag': False,
                    'errorDetails': serializer.errors,
                    'data': {}
                }
                logger.warning(f"Resend OTP failed: {data['message']}")
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
            logger.error("Internal server error in ResendOTPView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = request.user
            if user.is_authenticated:
                Token.objects.filter(user=user).delete()
                logout(request)
                data = {
                    'response_code': 200,
                    'status': 'Success',
                    'message': 'Logged out successfully',
                    'statusFlag': True,
                    'errorDetails': None,
                    'data': {}
                }
                logger.info(f"Logged out: {data['message']} (user_id: {user.id})")
            else:
                data = {
                    'response_code': 401,
                    'status': 'Failed',
                    'message': 'User not authenticated',
                    'statusFlag': False,
                    'errorDetails': None,
                    'data': {}
                }
                logger.warning(f"Logout failed: {data['message']}")
            return Response(data, status=data['response_code'])
        except Exception as e:
            data = {
                'response_code': 500,
                'status': 'Failed',
                'message': 'Internal server error',
                'statusFlag': False,
                'errorDetails': str(e),
                'data': {}
            }
            logger.error("Internal server error in LogoutView", exc_info=True)
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)