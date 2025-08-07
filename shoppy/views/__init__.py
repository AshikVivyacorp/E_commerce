from shoppy.views.regloginview import (
    RegisterView,
    LoginView,
<<<<<<< HEAD
    VerifyOTPView,
    ResendOTPView,
=======
    VerifyOTP,
    ResendOTP,
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
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
<<<<<<< HEAD
    ViewInvoicePDF
=======
    ViewInvoicePDFView
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
)

from shoppy.views.shipmentview import ShipmentStatusUpdateView

from shoppy.views.admindashboardview import (
    AdminDashboardSerializer,
    AdminDashboardView
)
