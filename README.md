# 🛒 E_commerce – Django-Based Online Store

**E_commerce** is a full-featured, modular Django e-commerce platform designed for scalability and real-world production use. It supports product listing, cart, checkout, order tracking, OTP/email-based authentication, admin controls, PDF invoice generation, and shipment tracking.

---

## 🚀 Features

- ✅ Product listing and detail pages
- ✅ Add to cart and checkout flow
- ✅ User login via email/OTP
- ✅ Admin panel for managing orders and products
- ✅ Shipment tracking updates linked with order status
- ✅ Auto-generated PDF invoices
- ✅ Custom API responses and centralized logging
- ✅ MySQL database support

---

## 🧱 Tech Stack

- **Backend**: Django, Django REST Framework
- **Auth**: Django Knox, OTP-based login
- **Database**: MySQL
- **PDF Generator**: ReportLab
- **Logging**: Python logging module with centralized `get_logger()`
- **API Responses**: Standardized via `build_response()` utility

---

## 🔧 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone git@github.com:AshikVivyacorp/E_commerce.git
   cd E_commerce
