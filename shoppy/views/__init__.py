from shoppy.views.regloginview import (
    RegisterView,
    LoginView,
    VerifyOTPView,
    ResendOTPView,
    LogoutView
)

from shoppy.views.productview import (
    IsAdminUser,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductRestockView
)

from shoppy.views.orderview import (
    CartView,
    PlaceCartOrderView,
    DirectOrderView,
    ViewInvoicePDF
)

from shoppy.views.shipmentview import ShipmentStatusUpdateView

from shoppy.views.admindashboardview import (
    AdminDashboardSerializer,
    AdminDashboardView
)
