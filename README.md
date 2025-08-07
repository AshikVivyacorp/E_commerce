<<<<<<< HEAD
# 🛒 E_commerce – Django-Based Online Store

**E_commerce** is a full-featured, modular Django e-commerce platform designed for scalability and real-world production use. It supports product listing, cart, checkout, order tracking, OTP/email-based authentication, admin controls, PDF invoice generation, and shipment tracking.
=======
# 🛒 E_commerce – Django-Based Online Shopping Platform

![Django](https://img.shields.io/badge/Django-4.x-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📖 Overview

**E_commerce** is a fully functional online shopping platform built with Django. It supports product browsing, cart management, secure checkout, user authentication, and admin control, making it ideal for educational purposes or commercial expansion.
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)

---

## 🚀 Features

<<<<<<< HEAD
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
=======
- ✅ User registration & login with OTP/email
- ✅ Product catalog with category filtering
- ✅ Shopping cart and checkout flow
- ✅ Order management and tracking
- ✅ PDF invoice generation
- ✅ Admin dashboard for product/orders
- ✅ REST API with custom responses
- ✅ Centralized logging with `get_logger()`

---

## ⚙️ Tech Stack

- **Backend:** Django (Python)
- **Database:** MySQL
- **Auth:** Django Knox
- **Frontend:** Django Templates or React (optional)
- **Others:** Logging, OTP login, PDF generation

---

## 🛠️ Local Setup Instructions

### 📦 Prerequisites

- Python 3.10+
- Git
- MySQL Server
- pip & virtualenv

---

### 🔧 Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/AshikVivyacorp/E_commerce.git
cd E_commerce

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure .env file
cp .env.example .env
# Update DB_NAME, DB_USER, DB_PASSWORD, etc.

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
>>>>>>> 987dbcd (Initial project setup with working Django e-commerce backend)
