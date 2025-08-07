from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema

from shoppy.models import User, OTP
from shoppy.serializer import (
    RegistrationSerializer, LoginSerializer,
    OTPVerifySerializer, ResendOTPSerializer
)
from shoppy.utils import generate_otp, send_otp_email, is_otp_valid, create_user_session


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            if User.objects.filter(email=email).exists():
                return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.validated_data["password"] = make_password(serializer.validated_data["password"])
            user = serializer.save()

            # ✅ Promote to admin if it's the predefined admin email
            if email == "admin@emarket.com":
                user.is_admin = True
                user.is_superuser = True
                user.is_staff = True
                user.save()

            otp = generate_otp()
            OTP.objects.create(user=user, code=otp)
            send_otp_email(email, otp)

            return Response({"message": "User registered. OTP sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer, security=[])
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found. Please register first."}, status=status.HTTP_404_NOT_FOUND)

            otp = generate_otp()
            OTP.objects.create(user=user, code=otp)
            send_otp_email(email, otp)

            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    @swagger_auto_schema(request_body=OTPVerifySerializer, security=[])
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_code = serializer.validated_data["otp"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "Invalid user. Please register first."}, status=status.HTTP_404_NOT_FOUND)

            if not is_otp_valid(user, otp_code):
                return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

            token = AuthToken.objects.create(user)[1]
            create_user_session(user, request)
            return Response({
                "message": "OTP verified successfully",
                "token": token
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOTP(APIView):
    @swagger_auto_schema(request_body=ResendOTPSerializer, security=[])
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found. Please register first."}, status=status.HTTP_404_NOT_FOUND)

            otp = generate_otp()
            OTP.objects.create(user=user, code=otp)
            send_otp_email(email, otp)
            return Response({"message": "OTP resent to your email"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(KnoxLogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        super().post(request, format=None)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
