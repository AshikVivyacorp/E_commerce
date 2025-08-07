from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from knox.models import AuthToken
from shoppy.models import User, OTP, Product, Order


class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.verify_otp_url = reverse('verify-otp')
        self.resend_otp_url = reverse('resend-otp')
        self.logout_url = reverse('logout')
        self.user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
            "address": "123 Street",
            "district": "Trichy",
            "state": "TN",
            "country": "India",
            "pincode": "620001",
            "phone": "9876543210"
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        User.objects.create(**self.user_data)
        response = self.client.post(self.login_url, {"email": self.user_data["email"]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_otp(self):
        user = User.objects.create(**self.user_data)
        OTP.objects.create(user=user, code="123456", created_at=timezone.now())
        payload = {"email": user.email, "otp": "123456"}
        response = self.client.post(self.verify_otp_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resend_otp(self):
        user = User.objects.create(**self.user_data)
        response = self.client.post(self.resend_otp_url, {"email": user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        user = User.objects.create(**self.user_data)
        _, token = AuthToken.objects.create(user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(
            name="Admin",
            email="admin@emarket.com",
            password="admin",
            address="Trichy",
            district="D",
            state="S",
            country="C",
            pincode="620001",
            phone="9876543210",
            is_admin=True,
            is_superuser=True
        )
        self.create_url = reverse('product-create')
        self.list_url = reverse('product-list')
        _, self.token = AuthToken.objects.create(self.admin)

    def test_create_product_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            "name": "Phone",
            "brand": "Samsung",
            "description": "Latest 5G phone",
            "price": "15000",
            "quantity": 10,
            "sold_count": 0
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="user@example.com",
            password="user123",
            address="123 Street",
            district="Trichy",
            state="TN",
            country="India",
            pincode="620001",
            phone="9876543210"
        )
        self.product = Product.objects.create(
            name="Laptop",
            brand="Dell",
            description="Latest i7 laptop",
            price=50000,
            quantity=5,
            sold_count=0
        )
        self.direct_url = reverse('direct-order')
        _, self.token = AuthToken.objects.create(self.user)

    def test_place_direct_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            "products": [{"product_id": self.product.id, "quantity": 1}],
            "confirm_dispatch": "yes",
            "payment_mode": "COD",
            "distance": 10
        }
        response = self.client.post(self.direct_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])


class ShipmentTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(
            name="Admin",
            email="admin@emarket.com",
            password="admin",
            address="Admin Street",
            district="Trichy",
            state="TN",
            country="India",
            pincode="620001",
            phone="9876543210",
            is_admin=True,
            is_superuser=True
        )
        self.user = User.objects.create(
            name="User",
            email="user@demo.com",
            password="userpass",
            address="User Street",
            district="X",
            state="Y",
            country="Z",
            pincode="987654",
            phone="9999999999"
        )
        self.order = Order.objects.create(
            user=self.user,
            invoice_id="INV001",
            total=15000,
            dispatch_address=self.user.address,
            dispatch_phone=self.user.phone,
            payment_status="COD"
        )
        self.shipment_url = reverse('update-shipment-status')
        _, self.token = AuthToken.objects.create(self.admin)

    def test_update_shipment_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        payload = {
            "order_id": self.order.id,
            "shipment_status": "Dispatched"
        }
        response = self.client.post(self.shipment_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Shipment status updated")


class DashboardTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(
            name="Admin",
            email="admin@emarket.com",
            password="admin",
            address="Admin Street",
            district="Trichy",
            state="TN",
            country="India",
            pincode="620001",
            phone="9876543210",
            is_admin=True,
            is_superuser=True
        )
        self.url = reverse('admin-dashboard')
        _, self.token = AuthToken.objects.create(self.admin)

    def test_admin_dashboard(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_users", response.data)
        self.assertIn("total_products", response.data)
        self.assertIn("total_orders", response.data)
