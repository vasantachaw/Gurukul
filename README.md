Gurukul Computer & Gurukul T-Plaa Shop

Project Overview
Gurukul Computer Institute & Gurukul T-Plaa Shop is a full-fledged web platform built using Python 3.10 and Django 5.0.0, designed to serve both educational and e-commerce needs. The platform is powered by Sajilolist and developed by Basant Chaw, co-founder of Sajilolist.

This project combines an online technical learning portal and a digital marketplace for computer, mobile, and electronics accessories. It enables students to enroll in online courses while also allowing users to buy and sell products ranging from PC components, peripherals, mobile phones, and accessories from A to Z.

Features
Educational Platform

Provides online technical courses for students in areas such as:

Web Development (Django, React, HTML/CSS)

Programming Languages (Python, Java, C++)

Networking and Hardware Basics

Software and App Development

Course content available via video lectures, downloadable notes, and assignments

Student dashboard for tracking progress, course completion, and certificates

Notifications for new courses, updates, and announcements

Real-time updates using Django Channels and WebSockets

Marketplace / Shop

Full e-commerce functionality for buying/selling electronics and tech devices:

PC Components (RAM, SSDs, Motherboards)

Peripherals (Keyboards, Mice, Monitors)

Mobile Devices and Accessories

Other electronics and gadgets

Product listings with detailed descriptions, images, and categories

Wishlist and Cart management

Payment integration with:

eSewa

Khalti

PayPal

Cash on Delivery

Order management and status tracking

Admin panel for managing products, orders, and users

Marketplace Features

Multi-category product support

Advanced filtering by category, price, and location

User account management (registration, login, profile)

Product reviews and ratings

Notifications for order updates and new products

Real-time product updates via WebSocket notifications

Technology Stack
Backend

Python 3.10

Django 5.0.0

Django Packages:

Django Channels (WebSockets / real-time updates)

Django REST Framework (optional APIs)

Celery (for async tasks, notifications)

Database: PostgreSQL / MySQL (configurable)

Payment Gateways: eSewa, Khalti, PayPal integration

Frontend

HTML5 / CSS3 / JavaScript

Bootstrap 5 for responsive design

Dynamic content updates with AJAX

Charting and visualization tools (optional)

Tools & Development

Version Control: Git & GitHub

Code Editor: VS Code / PyCharm

Virtual Environment: venv / pip

Image Handling: Pillow

Other Utilities: Django Crispy Forms / Form Validation

Deployment-ready with Docker (optional)

Additional Features

Multi-language support (optional)

Dynamic homepage with listings filtered by user location

Admin and user dashboards

Notifications for course updates and marketplace activities

Wishlist and cart management

SEO optimized product and course pages

Mobile-friendly and responsive design

Secure user authentication and role-based access

Real-time updates using WebSockets

Project Structure
gurukul_project/
├── main_app/               # Core app for homepage, courses, and products
├── accounts/               # User authentication and profiles
├── courses/                # Online technical courses
├── marketplace/            # E-commerce functionality
├── static/                 # CSS, JS, images
├── templates/              # HTML templates
├── media/                  # Uploaded images and files
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
└── README.md

Installation & Setup

Clone the repository:

git clone https://github.com/<yourusername>/gurukul_project.git
cd gurukul_project


Create virtual environment:

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Setup database:

python manage.py makemigrations
python manage.py migrate


Run the server:

python manage.py runserver


Visit http://127.0.0.1:8000 to access the platform.

Credits

Developer: Basant Chaw – Co-founder of Sajilolist

Powered by: Sajilolist

Design & Frontend Inspiration: Gurukul Computer Institute

License

This project is open-source under the MIT License.
