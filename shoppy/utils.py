import random
import string
from datetime import timedelta
from io import BytesIO

from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .models import OTP, Product, UserSession, Invoice, User, Cart

<<<<<<< HEAD
=======
import logging
import sys

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
_logger.addHandler(logging.StreamHandler(sys.stdout))

def build_response(response_code=200, status='Success', message='', data=None, errorDetails=None, statusFlag=True):
    return {
        'response_code': response_code,
        'status': status,
        'message': message,
        'statusFlag': statusFlag,
        'errorDetails': errorDetails,
        'data': data if data is not None else {}
    }

def get_logger():
    return _logger


>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
# ----------------------- OTP Functions -----------------------

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def is_otp_valid(user, otp_code):
    try:
        otp_obj = OTP.objects.filter(user=user, code=otp_code).latest('created_at')
        return timezone.now() <= otp_obj.created_at + timedelta(minutes=5)
    except OTP.DoesNotExist:
        return False

# ----------------------- Email Sending -----------------------

def send_otp_email(email, otp):
    subject = "E-Market OTP Verification"
    message = f"Your OTP is: {otp}. It is valid for 5 minutes."
    EmailMessage(subject, message, to=[email]).send()

<<<<<<< HEAD
def notify_admin_out_of_stock(product):
    subject = f"Product Out of Stock: {product.name}"
    message = f"The product '{product.name}' is out of stock."
    admin_email = "ashik1682003@gmail.com"
    EmailMessage(subject, message, to=[admin_email]).send()
=======

def notify_admin_out_of_stock(product):
    subject = f" Out of Stock Alert: {product.name}"
    message = (
        f"Dear Admin,\n\n"
        f"The product '{product.name}' is out of stock on E-Market.\n"
        f"Please restock it at the earliest.\n\n"
        f"Regards,\nE-Market System"
    )

    try:
        email_msg = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From
            ['ashik1682003@gmail.com']  # To: Admin email
        )
        email_msg.send(fail_silently=False)
        _logger.info(f"Out-of-stock email sent for product {product.name}")
    except Exception as e:
        _logger.error(f"Failed to send out-of-stock email for {product.name}: {e}")

>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)

def notify_users_product_restocked(product):
    subject = f"Product Restocked: {product.name}"
    message = f"The product '{product.name}' is now available again on E-Market. Hurry before it sells out!"
    users = User.objects.all()
    for user in users:
        EmailMessage(subject, message, to=[user.email]).send()

# ----------------------- Admin Check -----------------------

def is_admin(user):
    if isinstance(user, str):  # Handle email string
        return user == "admin@emarket.com"
    return user.email == "admin@emarket.com"

# ----------------------- PDF Invoice Generation -----------------------

def generate_invoice_pdf(order, order_items, total_amount, shipping_fee, payment_mode, gst_amount=None, cod_surcharge=None):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, "E-Market Invoice")
    y -= 30

    p.setFont("Helvetica", 10)
    p.drawString(50, y, "E-Market, Dummy Address, Trichy")
    y -= 15
    p.drawString(50, y, "Contact: 9876543210")
    y -= 30

    p.drawString(50, y, f"Invoice Date: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 15
    p.drawString(50, y, f"Order ID: {order.id}")
    p.drawString(300, y, f"User: {order.user.email}")
    y -= 30

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Items")
    y -= 20

    p.setFont("Helvetica", 10)
    for item in order_items:
        line = f"{item.product.name} - ₹{item.price} x {item.quantity} = ₹{item.price * item.quantity}"
        p.drawString(60, y, line)
        y -= 15
        if y < 100:
            p.showPage()
            y = height - 50

    y -= 20
    p.drawString(50, y, f"Subtotal: ₹{total_amount}")
    y -= 15
    p.drawString(50, y, f"Shipping Fee: ₹{shipping_fee}")
    if payment_mode.lower() == "cod" and cod_surcharge:
        y -= 15
        p.drawString(50, y, f"COD Surcharge: ₹{cod_surcharge}")
    if payment_mode.lower() == "online" and gst_amount:
        y -= 15
        p.drawString(50, y, f"GST (8%): ₹{gst_amount}")
    y -= 15
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total: ₹{order.total}")
    y -= 30

    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Shipping Address: {order.dispatch_address}")
    y -= 15
    p.drawString(50, y, f"Phone: {order.dispatch_phone}")
    y -= 30
    p.drawString(50, y, "Thank you for shopping with E-Market!")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# ----------------------- Save PDF to DB -----------------------

def save_invoice_pdf_to_model(order, pdf):
    filename = f"invoice_{order.id}.pdf"
    invoice = Invoice.objects.create(order=order, user=order.user, invoice_id=filename, total=order.total)
    invoice.pdf_file.save(filename, ContentFile(pdf))
    invoice.save()
    return invoice

# ----------------------- Send PDF Email -----------------------

def send_invoice_email(user_email, invoice_pdf, order_id):
    subject = f"E-Market Invoice for Order #{order_id}"
    message = "Please find attached your invoice for the recent order from E-Market."
    email = EmailMessage(subject, message, to=[user_email])
    email.attach(f"invoice_{order_id}.pdf", invoice_pdf, "application/pdf")
    email.send()

# ----------------------- User Session Management -----------------------

def create_user_session(user, request):
    session = UserSession.objects.create(
        user=user,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    return session

def end_user_session(user):
    UserSession.objects.filter(user=user).delete()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

# ----------------------- Cart Total -----------------------

def calculate_cart_total(user):
    cart_items = Cart.objects.filter(user=user)
    return sum(item.product.price * item.quantity for item in cart_items)
