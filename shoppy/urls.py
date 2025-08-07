from django.urls import path
from knox import views as knox_views
from shoppy.views.regloginview import (
<<<<<<< HEAD
    RegisterView, LoginView, VerifyOTPView,
    ResendOTPView, LogoutView
)

=======
    RegisterView, LoginView, VerifyOTP,
    ResendOTP, LogoutView
)
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
from shoppy.views.productview import (
    ProductListView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, ProductRestockView
)
<<<<<<< HEAD

from shoppy.views.orderview import CartView, PlaceCartOrderView, DirectOrderView
from shoppy.views.orderview import ViewInvoicePDFView

=======
from shoppy.views.orderview import (
    CartView, PlaceCartOrderView, DirectOrderView, ViewInvoicePDFView,
    RemoveCartItemView
)
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
from shoppy.views.shipmentview import ShipmentStatusUpdateView
from shoppy.views.admindashboardview import AdminDashboardView

urlpatterns = [
<<<<<<< HEAD
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Knox Auth (optional)
    path('knox-logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout-all'),

    # Products
=======
    # Auth routes
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTP.as_view(), name='resend-otp'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Knox auth optional
    path('knox-logout/', knox_views.LogoutView.as_view(), name='knox-logout'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout-all'),

    # Product routes
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/restock/<int:pk>/', ProductRestockView.as_view(), name='product-restock'),

<<<<<<< HEAD
    # Orders
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/place-order/', PlaceCartOrderView.as_view(), name='place-cart-order'),
    path('direct-order/', DirectOrderView.as_view(), name='direct-order'),

    # Invoices
    path('invoice/<int:order_id>/', ViewInvoicePDF.as_view(), name='view-invoice'),
=======
    # Cart & Order
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/remove/<int:id>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
    path('cart/place-order/', PlaceCartOrderView.as_view(), name='place-cart-order'),
    path('direct-order/', DirectOrderView.as_view(), name='direct-order'),

    # Invoice
    path('invoice/<int:order_id>/', ViewInvoicePDFView.as_view(), name='view-invoice'),
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)

    # Shipment
    path('admin/update-shipment-status/', ShipmentStatusUpdateView.as_view(), name='update-shipment-status'),

<<<<<<< HEAD
    # Admin Dashboard
=======
    # Dashboard
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
]
