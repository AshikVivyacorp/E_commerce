from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# -------------------- Custom User Manager --------------------

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

# -------------------- Unified User Model --------------------

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)
    district = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    pincode = models.CharField(max_length=10)

    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# -------------------- OTP --------------------

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.email} - {self.code}"

# -------------------- Product --------------------

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField()
    sold_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.brand})"

# -------------------- Cart --------------------

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} - {self.product.name} x {self.quantity}"

# -------------------- Order --------------------

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dispatch_confirmed = models.BooleanField(default=True)
    dispatch_address = models.TextField(blank=True)
    dispatch_phone = models.CharField(max_length=15, blank=True)

    shipment_status = models.CharField(
        max_length=30,
        choices=[
            ('Pending', 'Pending'),
            ('Dispatched', 'Dispatched'),
            ('In Transit', 'In Transit'),
            ('Delivered', 'Delivered')
        ],
        default='Pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('COD', 'Cash on Delivery'),
            ('Online', 'Online Payment')
        ],
        default='COD'
    )

    payment_mode = models.CharField(max_length=20, default='COD')
    distance = models.PositiveIntegerField(default=0)
    is_direct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = f"INV-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

# -------------------- Order Items --------------------

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

# -------------------- Invoice --------------------

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=100, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pdf_file = models.FileField(upload_to="invoices/")

    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.user.email}"

# -------------------- User Session --------------------

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"
