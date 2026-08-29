# 🛒 CodeAlpha E-Commerce Store

A full-featured E-Commerce Store web application developed using Django. This project was created as part of the **CodeAlpha Full Stack Development Internship Program**.

---

## 🚀 Features

### 🛍️ Product Management
- Display products on the home page
- Product detail page
- Product image support
- Product description
- Product price display
- Product stock management
- Product categories

### 🛒 Shopping Cart
- Add products to cart
- Increase product quantity
- Decrease product quantity
- Remove products from cart
- Automatic cart total calculation

### ❤️ Wishlist
- Add products to wishlist
- Remove products from wishlist
- Dedicated wishlist page

### 📦 Order Management
- Checkout functionality
- Customer information collection
- Order creation
- Order item management
- Order details page
- My Orders page
- Order cancellation functionality

### 💳 Payment
- Cash on Delivery option
- Payment method selection

### 📊 Admin Dashboard
- Product management
- Order overview
- Order status management
- Stock monitoring
- Sales information

### 📱 Responsive Design
- Mobile-friendly layout
- Responsive product pages
- Responsive admin dashboard

---

## 🛠️ Technologies Used

- Python
- Django
- HTML5
- CSS3
- SQLite
- JavaScript

---

## 📂 Project Structure

```text
CodeAlpha_EcommerceStore/
│
├── CodeAlpha_EcommerceStore/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── products/
│   ├── migrations/
│   ├── static/
│   │   └── products/
│   │       └── admin.css
│   │
│   ├── templates/
│   │   ├── admin/
│   │   │   └── base_site.html
│   │   │
│   │   └── products/
│   │       ├── home.html
│   │       ├── product_detail.html
│   │       ├── cart.html
│   │       ├── checkout.html
│   │       ├── order_success.html
│   │       ├── my_orders.html
│   │       ├── order_detail.html
│   │       ├── wishlist.html
│   │       └── admin_dashboard.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── manage.py