from django.contrib import admin
<<<<<<< HEAD
from .models import User, Product, Cart, Order, OrderItem, Invoice, OTP
=======
from .models import (
    User, Product, Cart, Order, OrderItem, Invoice, OTP, ShipmentTracking
)

# ------------------ Order Admin ------------------
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'invoice_id', 'payment_status', 'shipment_status', 'created_at']
    list_filter = ['shipment_status', 'payment_status']
    search_fields = ['user__email', 'invoice_id']
    list_editable = ['shipment_status']

<<<<<<< HEAD
admin.site.register(Order, OrderAdmin)

# Register other models
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Invoice)
admin.site.register(OTP)
=======

# ------------------ Shipment Tracking Admin ------------------

class ShipmentTrackingAdmin(admin.ModelAdmin):
    list_display = ['order', 'tracking_number', 'carrier', 'status', 'last_updated']
    list_filter = ['carrier', 'status']
    search_fields = ['tracking_number', 'order__invoice_id']
    ordering = ['-last_updated']


# ------------------ Register All Models ------------------

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Invoice)
admin.site.register(OTP)
admin.site.register(ShipmentTracking, ShipmentTrackingAdmin)
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
