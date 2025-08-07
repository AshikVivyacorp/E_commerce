from django.contrib import admin
from .models import User, Product, Cart, Order, OrderItem, Invoice, OTP

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'invoice_id', 'payment_status', 'shipment_status', 'created_at']
    list_filter = ['shipment_status', 'payment_status']
    search_fields = ['user__email', 'invoice_id']
    list_editable = ['shipment_status']

admin.site.register(Order, OrderAdmin)

# Register other models
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Invoice)
admin.site.register(OTP)
