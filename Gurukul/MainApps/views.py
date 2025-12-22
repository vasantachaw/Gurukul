import os
import re
import uuid
import json
import hmac
import hashlib
import base64
import requests
from io import BytesIO
from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from PIL import Image, ImageDraw, ImageFont

from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F, Q
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.files.base import ContentFile


from MainApps.models import (
    AboutUs,
    Website,
    PcPheripherals,
    Banner,
    Employee,
    PcPeripheralCart,
    Blog,
    OrderPlaced,
    OrderItem,
    CourseBooking,
    ContactMessage,
    Certificate,
    DigitalService,
    NewAdmissionApplication,
    Feedback,
)



def new_admission_applications(request):
    # -------------------- AUTHENTICATION CHECK --------------------
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to submit an admission form.")
        return redirect("user_login")

    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "phone_number": request.POST.get("phone_number"),
            "email": request.POST.get("email"),
            "date_of_birth": request.POST.get("date_of_birth"),
            "gender": request.POST.get("gender"),
            "religion": request.POST.get("religion"),
            "school_name": request.POST.get("school_name"),
            "postal_code": request.POST.get("postal_code"),
            "education_background": request.POST.get("education_background"),
            "course_id": request.POST.get("course"),
            "class_time": request.POST.get("class_time"),
            "class_mode": request.POST.get("class_mode"),
            "province": request.POST.get("province"),
            "district": request.POST.get("district"),
            "city": request.POST.get("city"),
            "address": request.POST.get("address"),
            "father_name": request.POST.get("father_name"),
            "mother_name": request.POST.get("mother_name"),
            "local_parent": request.POST.get("local_parent"),
            "parent_phone": request.POST.get("parent_phone"),
            "parent_email": request.POST.get("parent_email"),
            "note": request.POST.get("note"),
        }

        profile_picture = request.FILES.get("profile_picture")

        # -------------------- VALIDATION --------------------
        required_fields = {
            "First Name": data["first_name"],
            "Last Name": data["last_name"],
            "Phone Number": data["phone_number"],
            "Email": data["email"],
            "Postal Code": data["postal_code"],
            "Date of Birth": data["date_of_birth"],
            "Gender": data["gender"],
            "Religion": data["religion"],
            "School Name": data["school_name"],
            "Education Background": data["education_background"],
            "Course": data["course_id"],
            "Class Time": data["class_time"],
            "Class Mode": data["class_mode"],
            "Province": data["province"],
            "District": data["district"],
            "City": data["city"],
            "Address": data["address"],
            "Father Name": data["father_name"],
            "Mother Name": data["mother_name"],
            "Local Parent": data["local_parent"],
            "Parent Phone": data["parent_phone"],
        }

        for field, value in required_fields.items():
            if not value or value.strip() == "":
                messages.error(request, f"{field} is required.")
                return redirect("new_admission_form")

        try:
            validate_email(data["email"])
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return redirect("new_admission_form")

        if not data["phone_number"].isdigit() or not (7 <= len(data["phone_number"]) <= 15):
            messages.error(request, "Invalid phone number.")
            return redirect("new_admission_form")

        if not data["parent_phone"].isdigit() or not (7 <= len(data["parent_phone"]) <= 15):
            messages.error(request, "Invalid parent phone number.")
            return redirect("new_admission_form")

        if data["gender"] not in [g[0] for g in NewAdmissionApplication.GENDER_CHOICES]:
            messages.error(request, "Invalid gender selection.")
            return redirect("new_admission_form")

        if data["class_mode"] not in [c[0] for c in NewAdmissionApplication.COURSE_MODE_CHOICES]:
            messages.error(request, "Invalid class mode.")
            return redirect("new_admission_form")

        if data["class_time"] not in [t[0] for t in NewAdmissionApplication.CLASS_TIME_CHOICES]:
            messages.error(request, "Invalid class time.")
            return redirect("new_admission_form")

        # -------------------- DUPLICATE CHECK --------------------
        if NewAdmissionApplication.objects.filter(
            Q(user=request.user) & Q(email=data["email"])
        ).exists():
            messages.error(request, "You have already submitted an admission form with this email.")
            return redirect("new_admission_form")

        # -------------------- SAVE --------------------
        NewAdmissionApplication.objects.create(
            user=request.user,
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone_number"],
            date_of_birth=data["date_of_birth"],
            gender=data["gender"],
            father_name=data["father_name"],
            mother_name=data["mother_name"],
            address_street=data["address"],
            city=data["city"],
            state_province=data["province"],
            local_parents_name=data["local_parent"],
            local_parents_number=data["parent_phone"],
            religious=data["religion"],
            school_college_name=data["school_name"],
            education_level=data["education_background"],
            programs=data["course_id"],
            course_mode=data["class_mode"],
            class_time=data["class_time"],
            note=data["note"],
            profile_picture=profile_picture,
        )

        messages.success(request, "Your admission form has been submitted successfully!")
        return redirect("new_admission_form")

    # -------------------- GET REQUEST --------------------
    context = {
        "gender_choices": NewAdmissionApplication.GENDER_CHOICES,
        "class_time_choices": NewAdmissionApplication.CLASS_TIME_CHOICES,
        "course_mode_choices": NewAdmissionApplication.COURSE_MODE_CHOICES,
        "education_level_choices": NewAdmissionApplication.EDUCATION_LEVEL_CHOICES,
        "religion_choices": NewAdmissionApplication.RELIGION_CHOICES,
        "course_choices": PcPheripherals.objects.filter(item_type="course"),
    }

    return render(request, "MainApps/new-admission-form.html", context)

def check_certificate_status(request):
    return render(request, "MainApps/check-certificate.html")


def home(request):
    websites = Website.objects.all()
    banners = Banner.objects.filter(is_active=True).order_by("-created_at")[:5]
    pc_peripherals = (
        PcPheripherals.objects.filter(is_available=True, item_type="device")
        .prefetch_related("images")
        .order_by("-created_at")
    )
    best_ = PcPheripherals.objects.filter(for_type="Best").order_by("-created_at")
    courses = PcPheripherals.objects.filter(
        is_available=True, item_type="course"
    ).order_by("-created_at")
    admins = Employee.objects.filter(position="Admin", is_active=True).first()
    best_sellers = PcPheripherals.objects.filter(sold__gt=0).order_by("-sold")[:5]
    top_product = best_sellers[0] if best_sellers else None
    active_employees = Employee.objects.filter(
        department__in=["Developer", "Trainer", "Technician"], is_active=True
    )

    # Department-wise employees
    developer = next((e for e in active_employees if e.department == "Developer"), None)
    trainer = next((e for e in active_employees if e.department == "Trainer"), None)
    technician = next(
        (e for e in active_employees if e.department == "Technician"), None
    )
    shp_and_insitute=Feedback.SOURCE_CHOICES


    # Fetch public feedbacks for Shop
    shop_feedbacks = Feedback.objects.filter(is_public=True, source='shop').order_by('?')
    # Fetch public feedbacks for Institute
    institute_feedbacks = Feedback.objects.filter(is_public=True, source='institute').order_by('?')
    feedbacks=Feedback.objects.filter(is_public=True).order_by('-rating', '-created_at')

    context = {
        "websites": websites,
        "banners": banners,
        "pc_peripherals": pc_peripherals,
        "course": courses,
        "director": admins,
        "best": best_,
        "best_sellers": best_sellers,
        "developer": developer,
        "trainer": trainer,
        "technician": technician,
        "s_i": shp_and_insitute,
        "shop_feedbacks": shop_feedbacks,          # Add Shop feedbacks
        "feedbacks":feedbacks,
        "institute_feedbacks": institute_feedbacks,  # Add Institute feedbacks
        "blogs": Blog.objects.filter(is_published=True).order_by("-created_at")[:5],
    }

    return render(request, "MainApps/home.html", context)


def ProductList(request):
    selected_category = request.GET.get("category", "all")
    qs = PcPheripherals.objects.filter(is_available=True, item_type="device").order_by(
        "-created_at"
    )

    if selected_category != "all":
        qs = qs.filter(device_type=selected_category)

    # Pass all choice options from model
    device_choices = PcPheripherals.DEVICE_TYPES

    # Find readable label
    selected_label = "All"
    for val, lab in device_choices:
        if val == selected_category:
            selected_label = lab
            break

    return render(
        request,
        "MainApps/productList.html",
        {
            "product": qs,
            "selected_category": selected_category,
            "device_choices": device_choices,
            "selected_label": selected_label,
        },
    )


def CourseList(request):
    selected_level = request.GET.get("level", "all")

    # Filter only course items
    courses = PcPheripherals.objects.filter(
        is_available=True, item_type="course"
    ).order_by("-created_at")

    # Filter by course level
    if selected_level != "all":
        courses = courses.filter(course_level=selected_level)

    # Define available course levels
    COURSE_LEVELS = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    # Find readable label for selected level
    selected_label = "All"
    for val, lab in COURSE_LEVELS:
        if val == selected_level:
            selected_label = lab
            break

    return render(
        request,
        "MainApps/courseList.html",
        {
            "courses": courses,
            "selected_level": selected_level,
            "course_levels": COURSE_LEVELS,
            "selected_label": selected_label,
        },
    )


def Pc_ProductView(request, pk):
    product = get_object_or_404(PcPheripherals, pk=pk)
    PcPheripherals.objects.filter(pk=pk).update(views=F("views") + 1)
    product.refresh_from_db()

    cart_count = (
        PcPeripheralCart.objects.filter(
            user=request.user, pc_peri__device_type=product.device_type
        ).count()
        if request.user.is_authenticated
        else 0
    )

    related_products = PcPheripherals.objects.filter(
        device_type=product.device_type
    ).exclude(pk=product.pk)[:4]

    return render(
        request,
        "MainApps/productDetails.html",
        {
            "product": product,
            "cart_count": cart_count,
            "related_products": related_products,
        },
    )


def Bloglist(request):
    blog_list = Blog.objects.filter(is_published=True)
    paginator = Paginator(blog_list, 5)  # 5 blogs per page
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    return render(request, "MainApps/blogList.html", {"blogs": blogs})


def BlogDetailView(request, pk):
    blog = get_object_or_404(Blog, pk=pk, is_published=True)
    Blog.objects.filter(pk=pk).update(views=F("views") + 1)
    blog.refresh_from_db()
    related_blogs = Blog.objects.exclude(pk=blog.pk)[:4]
    return render(
        request,
        "MainApps/BlogDetail.html",
        {"blog": blog, "related_blogs": related_blogs},
    )


@login_required
def add_pc_to_cart(request, pc_id):
    pc = get_object_or_404(PcPheripherals, id=pc_id)
    cart_item, created = PcPeripheralCart.objects.get_or_create(
        user=request.user, pc_peri=pc, defaults={"quantity": 1}
    )
    message = "Added to your cart successfully." if created else "Already in your cart."
    return JsonResponse({"message": message})


@login_required
def plus_pc_cart(request):
    prod_id = request.GET.get("prod_id")
    cart_item = get_object_or_404(
        PcPeripheralCart, user=request.user, pc_peri_id=prod_id
    )
    cart_item.quantity += 1
    cart_item.save()

    cart_total = sum(
        item.total_cost for item in PcPeripheralCart.objects.filter(user=request.user)
    )
    return JsonResponse(
        {
            "quantity": cart_item.quantity,
            "total_price": float(cart_item.total_cost),
            "cart_total": float(cart_total),
        }
    )


@login_required
def minus_pc_cart(request):
    prod_id = request.GET.get("prod_id")
    try:
        cart_item = PcPeripheralCart.objects.get(user=request.user, pc_peri_id=prod_id)
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
            quantity = 0
            total_price = 0
        else:
            cart_item.save()
            quantity = cart_item.quantity
            total_price = float(cart_item.total_cost)
    except PcPeripheralCart.DoesNotExist:
        quantity = 0
        total_price = 0

    cart_total = sum(
        item.total_cost for item in PcPeripheralCart.objects.filter(user=request.user)
    )
    return JsonResponse(
        {
            "quantity": quantity,
            "total_price": total_price,
            "cart_total": float(cart_total),
        }
    )


@login_required
def remove_pc_from_cart(request, pk):
    cart_item = get_object_or_404(PcPeripheralCart, user=request.user, pk=pk)
    cart_item.delete()
    return JsonResponse({"message": "Successfully removed from your cart."})


def show_cart(request):
    if request.user.is_authenticated:
        pc_cart = PcPeripheralCart.objects.filter(user=request.user)
        total_cart_amount = sum(item.total_cost for item in pc_cart)
        total_cart_count = sum(item.quantity for item in pc_cart)
    else:
        pc_cart = []
        total_cart_amount = 0.0
        total_cart_count = 0
        messages.warning(request, "You must log in to view your cart!")

    return render(
        request,
        "MainApps/view-cart.html",
        {
            "pc_cart_items": pc_cart,
            "total_cart_amount": total_cart_amount,
            "total_cart_count": total_cart_count,
        },
    )


# ------------------------------
# CHECKOUT & ORDER VIEWS
# ------------------------------
def CheckOut(request):
    if request.user.is_authenticated:
        pc_cart = PcPeripheralCart.objects.filter(user=request.user)
        total_cart_amount = sum(float(item.total_cost) for item in pc_cart)
        total_cart_count = sum(item.quantity for item in pc_cart)  # total items in cart
    else:
        pc_cart = []
        total_cart_amount = 0.0
        total_cart_count = 0
    return render(
        request,
        "MainApps/checkout.html",
        context={
            "pc_cart": pc_cart,
            "total_cart_amount": total_cart_amount,
            "total_cart_count": total_cart_count,
        },
    )


def shipping_and_delivery_info(request):
    return render(request, "MainApps/shipping-delivery.html")


def search_query(request):
    query = request.GET.get("q", "")  # Get the search term from ?q= in URL
    item_type = request.GET.get("type", "")  # Optional: filter by device/course

    results = PcPheripherals.objects.all()

    if query:
        results = results.filter(
            Q(name__icontains=query)
            | Q(brand__icontains=query)
            | Q(device_type__icontains=query)
            | Q(item_type__icontains=query)
            | Q(instructor_name__icontains=query)
        )

    if item_type:
        results = results.filter(item_type=item_type)

    context = {
        "query": query,
        "item_type": item_type,
        "results": results,
    }
    return render(request, "MainApps/home-search.html", context)


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        messages.success(
            request, "Thank you for contacting us! We'll get back to you soon."
        )
        return redirect(
            "contact"
        )  # Redirect to the same page (or another success page)

    return render(request, "MainApps/contact.html")


def buy_now(request, pk):
    product = get_object_or_404(PcPheripherals, pk=pk)

    # Increment view count
    PcPheripherals.objects.filter(pk=pk).update(views=F("views") + 1)

    if request.user.is_authenticated:
        # Add item to cart
        PcPeripheralCart.objects.get_or_create(
            user=request.user, pc_peri=product, defaults={"quantity": 1}
        )
        # Return JSON indicating success and redirect URL
        return JsonResponse(
            {
                "status": "ok",
                "redirect_url": "/checkout/",  # Replace with your checkout URL
                "message": f"{product.name} has been added. Redirecting to checkout...",
            }
        )
    else:
        # User not logged in
        return JsonResponse(
            {
                "status": "login_required",
                "message": "You must log in to buy this product.",
            }
        )


# In MainApps/views.py


@login_required
def place_order(request):
    if request.method != "POST":
        return redirect("checkout")  # Ensure only POST is accepted

    # ... (Code to get form data like full_name, email, payment_method, etc.) ...
    payment_method = request.POST.get("payment_method", "").strip()

    # ... (Code to check cart, calculate total_amount) ...

    # --------------------------
    # Create Order (This is crucial, it must happen first)
    # --------------------------
    order = OrderPlaced.objects.create(
        # ... (Order data fields) ...
        payment_method=payment_method,
        # ...
    )

    # --------------------------
    # Create Order Items + Decrease stock + Clear Cart
    # --------------------------
    # ... (Your existing logic for OrderItem.objects.bulk_create and cart_items.delete()) ...

    # --------------------------
    # Handle Payment Method Redirection
    # --------------------------
    if payment_method == "cod":
        # 🟢 For COD, the payment is "confirmed" upon order creation.
        messages.success(
            request, "Your Cash on Delivery order has been placed successfully!"
        )
        return redirect(
            "view_cart"
        )  # Redirect to the cart view (you may want to change this to a success page)

    elif payment_method == "khalti":
        # ➡️ Redirect to Khalti view which will expect the order details (often via session/query params)
        messages.success(request, "Order placed. Redirecting to Khalti for payment...")
        return redirect("khalti_payment")

    # Handle other methods (e.g., eSewa, PayPal) similarly.

    # Fallback in case of unknown payment method
    messages.warning(request, "Order placed, but payment method requires attention.")
    return redirect("view_cart")


def about_us(request):
    # Fetch single entries for each section type
    gurukul = AboutUs.objects.filter(type="gurukul", is_active=True).first()
    vision = AboutUs.objects.filter(type="vision", is_active=True).first()
    mission = AboutUs.objects.filter(type="mission", is_active=True).first()
    study_env = AboutUs.objects.filter(type="study_env", is_active=True).first()
    established = AboutUs.objects.filter(type="established", is_active=True).first()

    # Fetch multiple lab entries
    labs = AboutUs.objects.filter(
        type__in=["hardware_lab", "computer_lab"], is_active=True
    )

    context = {
        "gurukul": gurukul,
        "vision": vision,
        "mission": mission,
        "labs": labs,
        "study_env": study_env,
        "established": established,
        "blogs": Blog.objects.filter(is_published=True).order_by("-created_at")[:5],
    }

    return render(request, "MainApps/about-us.html", context)


def courseBooking(request):
    admins = Employee.objects.filter(
        position="Admin", department="Trainer", is_active=True
    ).first()
    detail = Website.objects.first()
    class_time_choices = CourseBooking.CLASS_TIME_CHOICES
    course_mode_choices = CourseBooking.COURSE_MODE_CHOICES
    courses = PcPheripherals.objects.filter(item_type="course")

    if request.method == "POST":

        # 🔥 Handle unauthenticated user
        if not request.user.is_authenticated:
            messages.error(request, "Please login to book a course.")
            return redirect("course_booking")

        # Now user is always authenticated
        user = request.user

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        course_id = request.POST.get("course")
        class_time = request.POST.get("class_time")
        course_mode = request.POST.get("course_mode")
        note = request.POST.get("note")

        try:
            course_obj = PcPheripherals.objects.get(id=course_id)
            course_name = course_obj.name
        except PcPheripherals.DoesNotExist:
            messages.error(request, "Selected course not found.")
            return redirect("course_booking")

        # 🔥 Prevent duplicate booking
        if CourseBooking.objects.filter(user=user, course=course_name).exists():
            messages.warning(request, f"You have already booked {course_name}.")
            return redirect("course_booking")

        # Create booking
        CourseBooking.objects.create(
            user=user,
            course=course_name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            class_time=class_time,
            course_mode=course_mode,
            note=note,
        )

        messages.success(request, f"Booking successful for {course_name}!")
        return redirect("course_booking")

    context = {
        "employees": admins,
        "class_time_choices": class_time_choices,
        "course_mode_choices": course_mode_choices,
        "courses": courses,
        "detail": detail,
    }
    return render(request, "MainApps/courseBooking.html", context)


# def certificate_page(request):
#     if request.user.is_authenticated:
#         # Check if the user has a certificate
#         certificate_exists = Certificate.objects.filter(user=request.user).exists()
#         context = {
#             "certificate_exists": certificate_exists,
#             "user_authenticated": True,
#         }
#     else:
#         # User is not logged in
#         context = {
#             "certificate_exists": False,
#             "user_authenticated": False,
#         }
#     return render(request, "MainApps/certificate.html", context)


# def cetificate_verify(request):
#     if not request.user.is_authenticated:
#         return HttpResponse("Please login first!", status=401)

#     # Latest booking
#     booking = CourseBooking.objects.filter(user=request.user).last()
#     if not booking:
#         return HttpResponse("No course booking found for this user.", status=404)

#     student_name = f"{booking.first_name} {booking.last_name}"
#     course_name = booking.course

#     # Latest certificate
#     certificate = Certificate.objects.filter(user=request.user).last()
#     if not certificate:
#         return HttpResponse("No certificate found for this user.", status=404)

#     issue_date = certificate.issue_date.strftime("%d/%m/%Y")
#     certificate_no = certificate.certificate_no

#     # Fetch certificate template
#     template_obj = Website.objects.filter(certificate__isnull=False).first()
#     if not template_obj:
#         return HttpResponse("No certificate template found.", status=404)

#     # Open image
#     image = Image.open(template_obj.certificate.path)
#     draw = ImageDraw.Draw(image)

#     # Use a TTF font for larger sizes
#     font_path = os.path.join(settings.BASE_DIR, "static/fonts/Arial.ttf")
#     font_large = ImageFont.truetype(font_path, 60)  # student name
#     font_medium = ImageFont.truetype(font_path, 40)  # course name
#     font_small = ImageFont.truetype(font_path, 25)  # issue date & certificate number

#     W, H = image.size

#     def center_text(text, font, y):
#         bbox = draw.textbbox((0, 0), text, font=font)
#         text_width = bbox[2] - bbox[0]
#         x = (W - text_width) / 2
#         draw.text((x, y), text, fill="gray", font=font)

#     center_text(student_name, font_large, 750)
#     center_text(course_name, font_medium, 920)
#     draw.text((1785, 40), issue_date, fill="gray", font=font_small)
#     draw.text((285, 40), f"{certificate_no}", fill="gray", font=font_small)

#     buffer = BytesIO()
#     image.save(buffer, format="PNG")
#     buffer.seek(0)
#     return HttpResponse(buffer, content_type="image/png")


def khalti_payment(request):
    return HttpResponse("Khalti Payment Function Called")


def service_pricing(request):
    # Fetch all active services
    services = DigitalService.objects.filter(is_active=True).order_by(
        "category", "name"
    )

    # Group services by category
    grouped_services = defaultdict(list)
    for service in services:
        grouped_services[service.category].append(service)

    context = {
        "grouped_services": dict(
            grouped_services
        )  # Convert defaultdict to dict for template
    }
    return render(request, "MainApps/softpricing.html", context)


# Allow only admin/staff
def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    # GET parameters
    search = request.GET.get("search", "")
    payment_filter = request.GET.get("payment_method", "")
    status_filter = request.GET.get("order_status", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    # Base queryset
    orders = OrderPlaced.objects.all().order_by("-created_at")

    # Search
    if search:
        orders = orders.filter(
            Q(order_code__icontains=search)
            | Q(user__username__icontains=search)
            | Q(full_name__icontains=search)
        )

    # Filter by payment method
    if payment_filter:
        orders = orders.filter(payment_method=payment_filter)

    # Filter by order status
    if status_filter:
        orders = orders.filter(order_status=status_filter)

    # Filter by date range
    if start_date and end_date:
        orders = orders.filter(
            created_at__date__gte=start_date, created_at__date__lte=end_date
        )
    elif start_date:
        orders = orders.filter(created_at__date__gte=start_date)
    elif end_date:
        orders = orders.filter(created_at__date__lte=end_date)

    # Pagination (10 orders per page)
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    orders = paginator.get_page(page_number)

    context = {
        "orders": orders,
        "search": search,
        "payment_filter": payment_filter,
        "status_filter": status_filter,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "MainApps/admin-order.html", context)


@user_passes_test(is_admin)
def invoice_view(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    websites = Website.objects.all().first()
    print(websites)
    context = {
        "order": order,
        "order_items": order_items,
        "websites": websites,
    }
    return render(request, "MainApps/invoice.html", context)


ALLOWED_PAYMENT_METHODS = {"esewa", "khalti", "paypal", "bank", "cod"}


# ============================================================
#   CHECKOUT → PAYMENT CONFIRMATION (SECURE VALIDATION)
# ============================================================


@require_POST
def cod_confirmation(request):
    """
    Secure checkout confirmation endpoint.
    Validates + sanitizes all inputs before storing in session.
    """

    # -------- Validate Payment Method --------
    payment_method = request.POST.get("payment_method", "").lower().strip()
    if payment_method not in ALLOWED_PAYMENT_METHODS:
        return HttpResponseBadRequest("Invalid payment method")

    # -------- Required Fields --------
    required_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "province",
        "district",
        "city",
        "address",
    ]

    for field in required_fields:
        value = request.POST.get(field, "").strip()
        if not value:
            return HttpResponseBadRequest(f"Missing required field: {field}")

    # -------- Validate Email Format --------
    email = request.POST["email"].strip()
    try:
        validate_email(email)
    except ValidationError:
        return HttpResponseBadRequest("Invalid email format")

    # -------- Strong Input Sanitizer --------
    def clean(value):
        value = str(value)
        value = re.sub(r"[<>]", "", value)  # remove HTML tags
        value = value.strip()
        return value

    data = {
        "first_name": clean(request.POST["first_name"]),
        "last_name": clean(request.POST["last_name"]),
        "email": clean(email),
        "phone": clean(request.POST["phone"]),
        "province": clean(request.POST["province"]),
        "district": clean(request.POST["district"]),
        "city": clean(request.POST["city"]),
        "address": clean(request.POST["address"]),
        "note": clean(request.POST.get("note", "")),
        "payment_method": payment_method,
        "my_date": datetime.now(),
    }

    # -------- Session Safe Store (JSON safe) --------
    safe_session = data.copy()
    safe_session["my_date"] = safe_session["my_date"].isoformat()

    request.session["checkout_data"] = safe_session
    request.session.modified = True

    return render(request, "MainApps/payment-confirmation.html", data)


def cod_payment(request):

    checkout_data = request.session.get("checkout_data")
    if not checkout_data:
        print("❌ ERROR: Checkout data missing in session.")
        return HttpResponseBadRequest("Checkout session expired or missing")

    full_name = (
        f"{checkout_data.get('first_name')} {checkout_data.get('last_name')}".strip()
    )
    email = checkout_data.get("email")
    phone = checkout_data.get("phone")
    province = checkout_data.get("province")
    district = checkout_data.get("district")
    city = checkout_data.get("city")
    address = checkout_data.get("address")
    payment_method = checkout_data.get("payment_method")
    note = checkout_data.get("note")

    cart_items = PcPeripheralCart.objects.filter(user=request.user)
    if not cart_items.exists():
        message = {"status": "error", "message": "Your cart is empty!"}

        # AJAX case
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(message, status=400)

        messages.error(request, message["message"])
        return redirect("view_cart")  # <-- Replace with your cart url name

    # Calculate total
    total_amount = sum(
        item.pc_peri.discount_price * item.quantity for item in cart_items
    )

    # Create order
    order = OrderPlaced.objects.create(
        user=request.user,
        full_name=full_name,
        email=email,
        phone=phone,
        province=province,
        district=district,
        city=city,
        address=address,
        payment_method=payment_method,
        transaction_id=str(uuid.uuid4()),
        total_transaction_amount=total_amount,
        transaction_status="Pending",
        note=note,
        order_code=f"GITP-{uuid.uuid4().hex[:6].upper()}",
    )

    # Create order items + update stock & sold
    order_items = []
    for item in cart_items:
        peripheral = item.pc_peri

        # Decrease stock
        if peripheral.stock >= item.quantity:
            peripheral.stock -= item.quantity
        else:
            peripheral.stock = 0

        # Increase sold
        peripheral.sold = (peripheral.sold or 0) + item.quantity
        peripheral.save(update_fields=["stock", "sold"])

        order_items.append(
            OrderItem(
                order=order,
                item_type=item.pc_peri.item_type,
                peripheral=item.pc_peri,
                quantity=item.quantity,
            )
        )

    OrderItem.objects.bulk_create(order_items)

    # Clear cart
    cart_items.delete()

    # AJAX response
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "status": "success",
                "message": "Your order has been placed successfully!",
                "redirect_url": reverse("cod_success", args=[order.id]),
            },
            status=200,
        )

    return redirect("cod_success", order.id)


def cod_success(request, order_id):
    """
    Handle Cash on Delivery (COD) success page.
    """
    try:
        order = OrderPlaced.objects.get(id=order_id, user=request.user)

        # Update transaction status to Pending/Confirmed
        order.transaction_status = "Pending"  # or "Confirmed" if you want
        order.save(update_fields=["transaction_status"])

        # Clear user's cart after order placement
        PcPeripheralCart.objects.filter(user=request.user).delete()

        # Prepare data dictionary for template
        payment_data = {
            "payment_method": order.payment_method,
            "order_code": order.order_code,
            "total_amount": float(order.total_transaction_amount),
            "transaction_id": "N/A",  # COD doesn't have a transaction ID
        }

        # Render the success page
        return render(
            request,
            "MainApps/payment-successfully.html",
            {"data": payment_data},
        )

    except OrderPlaced.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect("cart")  # Make sure this URL name matches your cart view


# ============================================================
#   PAYMENT ROUTER / GATEWAY DECISION (HARD SECURITY)
# ============================================================


def payment_methods(request):
    checkout_data = request.session.get("checkout_data")
    if not checkout_data:
        return redirect("checkout")

    method = checkout_data.get("payment_method")
    if method == "paypal":
        return redirect("paypal_payment")
    if method == "esewa":
        return redirect("esewa_payment_view")
    if method == "khalti":
        return redirect("khalti_payment")
    if method == "cod":
        return redirect("cash_on_delivery")

    return redirect("checkout")


def paypal_payment(request):
    checkout_data = request.session.get("checkout_data")
    if not checkout_data:
        return redirect("checkout")

    # Example: print specific fields in console
    print("Full Name:", checkout_data.get("first_name"), checkout_data.get("last_name"))
    print("Email:", checkout_data.get("email"))
    print("Payment Method:", checkout_data.get("payment_method"))

    # Print all fields in browser
    output = ""
    for key, value in checkout_data.items():
        output += f"{key}: {value}\n"

    return HttpResponse(f"<pre>{output}</pre>")


def payment_successful(request):
    return render(request, "MainApps/payment-successfully.html")


##Genrating Signature for Esewa Transaction
def generate_signature(data_dict, secret_key):
    fields = data_dict["signed_field_names"].split(",")
    signed_data = ",".join(f"{field}={data_dict[field]}" for field in fields)
    signature = hmac.new(
        key=secret_key.encode("utf-8"),
        msg=signed_data.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(signature).decode()


@require_POST
def cod_confirmation(request):
    """
    Secure checkout confirmation endpoint.
    Validates + sanitizes all inputs before storing in session.
    """

    # -------- Validate Payment Method --------
    payment_method = request.POST.get("payment_method", "").lower().strip()
    if payment_method not in ALLOWED_PAYMENT_METHODS:
        return HttpResponseBadRequest("Invalid payment method")

    # -------- Required Fields --------
    required_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "province",
        "district",
        "city",
        "address",
    ]

    for field in required_fields:
        value = request.POST.get(field, "").strip()
        if not value:
            return HttpResponseBadRequest(f"Missing required field: {field}")

    # -------- Validate Email Format --------
    email = request.POST["email"].strip()
    try:
        validate_email(email)
    except ValidationError:
        return HttpResponseBadRequest("Invalid email format")

    # -------- Strong Input Sanitizer --------
    def clean(value):
        value = str(value)
        value = re.sub(r"[<>]", "", value)  # remove HTML tags
        value = value.strip()
        return value

    data = {
        "first_name": clean(request.POST["first_name"]),
        "last_name": clean(request.POST["last_name"]),
        "email": clean(email),
        "phone": clean(request.POST["phone"]),
        "province": clean(request.POST["province"]),
        "district": clean(request.POST["district"]),
        "city": clean(request.POST["city"]),
        "address": clean(request.POST["address"]),
        "note": clean(request.POST.get("note", "")),
        "payment_method": payment_method,
        "my_date": datetime.now(),
    }

    # -------- Session Safe Store (JSON safe) --------
    safe_session = data.copy()
    safe_session["my_date"] = safe_session["my_date"].isoformat()

    request.session["checkout_data"] = safe_session
    request.session.modified = True

    return render(request, "MainApps/payment-confirmation.html", data)


def esewa_payment_view(request):
    checkout_data = request.session.get("checkout_data")
    if not checkout_data:
        messages.error(request, "Checkout session has expired.")
        return redirect("cart")

    cart_items_qs = PcPeripheralCart.objects.filter(user=request.user)
    if not cart_items_qs.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("cart")

    # Calculate totals
    total = 0
    cart_items = []
    for cart_item in cart_items_qs:
        product = cart_item.pc_peri
        subtotal = product.discount_price * cart_item.quantity
        total += subtotal
        cart_items.append(
            {"product": product, "quantity": cart_item.quantity, "subtotal": subtotal}
        )

    service_charge = 20
    shipping_charge = 50
    grand_total = int(total + service_charge + shipping_charge)

    # Extract customer details
    full_name = (
        f"{checkout_data.get('first_name')} {checkout_data.get('last_name')}".strip()
    )
    email = checkout_data.get("email")
    phone = checkout_data.get("phone")
    province = checkout_data.get("province")
    district = checkout_data.get("district")
    city = checkout_data.get("city")
    address = checkout_data.get("address")
    note = checkout_data.get("note")

    # Create order
    order = OrderPlaced.objects.create(
        user=request.user,
        full_name=full_name,
        email=email,
        phone=phone,
        province=province,
        district=district,
        city=city,
        address=address,
        note=note,
        payment_method="esewa",
        transaction_status="Pending",
        total_transaction_amount=grand_total,
        transaction_id=str(uuid.uuid4()),
        order_code=f"GITP-{uuid.uuid4().hex[:6].upper()}",
    )

    # Save order items + update stock
    order_items = []
    for cart_item in cart_items_qs:
        product = cart_item.pc_peri
        product.stock = max(0, product.stock - cart_item.quantity)
        product.sold = (product.sold or 0) + cart_item.quantity
        product.save(update_fields=["stock", "sold"])

        order_items.append(
            OrderItem(
                order=order,
                item_type=product.item_type,
                peripheral=product,
                quantity=cart_item.quantity,
            )
        )
    OrderItem.objects.bulk_create(order_items)
    # Clear cart

    # eSewa Payment Payload
    transaction_uuid = str(uuid.uuid4())
    data = {
        "amount": str(grand_total),
        "tax_amount": "0",
        "total_amount": str(grand_total),
        "transaction_uuid": transaction_uuid,
        "product_code": "EPAYTEST",
        "product_service_charge": "0",
        "product_delivery_charge": "0",
        # Pass order_id as query param for success/failure URL
        "success_url": f"{settings.ESEWA_SUCCESS_URL}?order_id={order.id}",
        "failure_url": f"{settings.ESEWA_FAILURE_URL}?order_id={order.id}",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
    }
    data["signature"] = generate_signature(data, settings.ESEWA_SECRET_KEY)

    # Render payment page
    return render(
        request,
        "MainApps/payment/esewa.html",
        {
            "data": data,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "district": district,
            "province": province,
            "note": note,
            "payment_method": "esewa",
            "total_cart_count": cart_items_qs.count(),
            "total_cart_amount": total,
            "grand_total": grand_total,
            "cart_items": cart_items,
            "order": order,
        },
    )


def esewa_payment_success(request):
    """
    Handle eSewa payment success callback.
    """
    order_id = request.GET.get("order_id", "")
    order_id = order_id.split("?")[0].strip()

    try:
        order = OrderPlaced.objects.get(id=order_id)
        order.transaction_status = "Completed"
        order.save(update_fields=["transaction_status"])

        # Clear cart for logged-in user
        if request.user.is_authenticated:
            PcPeripheralCart.objects.filter(user=request.user).delete()

        payment_data = {
            "payment_method": order.payment_method,
            "order_code": order.order_code,
            "total_amount": float(order.total_transaction_amount),
            "transaction_id": str(order.transaction_id),
        }

        return render(
            request,
            "MainApps/payment-successfully.html",
            {"data": payment_data},
        )

    except OrderPlaced.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect("view_cart")


def khalti_confirm(request):
    """
    Secure checkout confirmation endpoint.
    Validates + sanitizes all inputs before storing in session.
    """

    # -------- Validate Payment Method --------
    payment_method = request.POST.get("payment_method", "").lower().strip()
    if payment_method not in ALLOWED_PAYMENT_METHODS:
        return HttpResponseBadRequest("Invalid payment method")

    # -------- Required Fields --------
    required_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "province",
        "district",
        "city",
        "address",
    ]

    for field in required_fields:
        value = request.POST.get(field, "").strip()
        if not value:
            return HttpResponseBadRequest(f"Missing required field: {field}")

    # -------- Validate Email Format --------
    email = request.POST["email"].strip()
    try:
        validate_email(email)
    except ValidationError:
        return HttpResponseBadRequest("Invalid email format")

    # -------- Strong Input Sanitizer --------
    def clean(value):
        value = str(value)
        value = re.sub(r"[<>]", "", value)  # remove HTML tags
        value = value.strip()
        return value

    data = {
        "first_name": clean(request.POST["first_name"]),
        "last_name": clean(request.POST["last_name"]),
        "email": clean(email),
        "phone": clean(request.POST["phone"]),
        "province": clean(request.POST["province"]),
        "district": clean(request.POST["district"]),
        "city": clean(request.POST["city"]),
        "address": clean(request.POST["address"]),
        "note": clean(request.POST.get("note", "")),
        "payment_method": payment_method,
        "my_date": datetime.now(),
    }

    # -------- Session Safe Store (JSON safe) --------
    safe_session = data.copy()
    safe_session["my_date"] = safe_session["my_date"].isoformat()

    request.session["checkout_data"] = safe_session
    request.session.modified = True

    return render(request, "MainApps/payment/khalti.html", data)


def khalti_payment_view(request):
    """
    Initiates Khalti Server-to-Server payment.
    Creates a pending order and redirects the user to the Khalti payment gateway URL.
    """
    if request.method != "POST":
        # Ensure this view is only accessed via a POST request from the confirmation page
        messages.error(request, "Invalid request method.")
        return redirect("cart")

    # 1. Validate Session Data and Authentication
    if not request.user.is_authenticated:
        messages.error(request, "You must log in to proceed with payment.")
        return redirect("login")

    checkout_data = request.session.get("checkout_data")
    if not checkout_data:
        messages.error(request, "Checkout session has expired.")
        return redirect("cart")

    # 2. Validate Cart
    cart_items_qs = PcPeripheralCart.objects.filter(user=request.user)
    if not cart_items_qs.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("cart")

    # 3. Calculate Totals and Prepare Product Details
    total = Decimal("0.00")
    product_details = []

    for cart_item in cart_items_qs:
        product = cart_item.pc_peri
        subtotal = product.discount_price * cart_item.quantity
        total += subtotal

        # Prepare product details for Khalti payload (amount must be in paisa)
        product_details.append(
            {
                "identity": str(product.id),
                "name": product.name,
                "total_price": int(subtotal * 100),  # paisa
                "quantity": cart_item.quantity,
                "unit_price": int(product.discount_price * 100),  # paisa
            }
        )

    service_charge = Decimal("20.00")
    shipping_charge = Decimal("50.00")
    grand_total = total + service_charge + shipping_charge
    grand_total = int(grand_total)  # Convert to integer for clean Rs value

    # 4. Extract Customer Details
    full_name = (
        f"{checkout_data.get('first_name')} {checkout_data.get('last_name')}".strip()
    )
    email = checkout_data.get("email")
    phone = checkout_data.get("phone")
    province = checkout_data.get("province")
    district = checkout_data.get("district")
    city = checkout_data.get("city")
    address = checkout_data.get("address")
    note = checkout_data.get("note")

    # 5. Create Order (Pending Status)
    order = OrderPlaced.objects.create(
        user=request.user,
        full_name=full_name,
        email=email,
        phone=phone,
        province=province,
        district=district,
        city=city,
        address=address,
        note=note,
        payment_method="khalti",
        transaction_status="Pending",
        total_transaction_amount=grand_total,
        transaction_id=str(uuid.uuid4()),  # Placeholder UUID
        order_code=f"GITP-{uuid.uuid4().hex[:6].upper()}",
    )

    # 6. Save Order Items + Update Stock
    order_items = []
    for cart_item in cart_items_qs:
        product = cart_item.pc_peri

        # Deduct Stock
        product.stock = max(0, product.stock - cart_item.quantity)
        product.sold = (product.sold or 0) + cart_item.quantity
        product.save(update_fields=["stock", "sold"])

        # Create Order Item
        order_items.append(
            OrderItem(
                order=order,
                item_type=product.item_type,
                peripheral=product,
                quantity=cart_item.quantity,
            )
        )
    OrderItem.objects.bulk_create(order_items)

    # 7. Prepare Khalti Payload and Initiate Server-to-Server Payment

    total_amount_paisa = grand_total * 100
    return_url = f"{settings.KHALTI_SUCCESS_URL}?order_id={order.id}"
    KHALTI_INITIATE_URL = "https://a.khalti.com/api/v2/epayment/initiate/"

    payload = {
        "return_url": return_url,
        "website_url": request.build_absolute_uri("/"),
        "amount": total_amount_paisa,
        "purchase_order_id": str(order.id),
        "purchase_order_name": f"Order {order.order_code}",
        "customer_info": {"name": full_name, "email": email, "phone": phone},
        "product_details": product_details,
    }

    headers = {
        # Secret key is required for authentication (resolves 401 error)
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(KHALTI_INITIATE_URL, headers=headers, json=payload)
        new_res = response.json()

        if response.status_code == 200:
            # Khalti returns a 'payment_url' to redirect the user to
            return redirect(new_res["payment_url"])
        else:
            # Handle API errors
            messages.error(
                request,
                f"Khalti initiation failed. Details: {new_res.get('detail', new_res)}",
            )
            order.delete()
            return redirect("cart")

    except requests.exceptions.RequestException as e:
        messages.error(request, "Connection to Khalti API failed.")
        order.delete()
        return redirect("cart")


def khalti_payment_success(request):
    """
    Handles Khalti payment success callback.
    Verifies the transaction status using the Khalti Lookup API.
    """
    # 1. Get Params from URL
    pidx = request.GET.get("pidx")
    order_id = request.GET.get("order_id")

    if not pidx or not order_id:
        messages.error(request, "Invalid payment parameters.")
        return redirect("cart")

    # 2. Verify Payment Status using Khalti Lookup API
    KHALTI_LOOKUP_URL = "https://a.khalti.com/api/v2/epayment/lookup/"

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    lookup_payload = {"pidx": pidx}

    try:
        response = requests.post(
            KHALTI_LOOKUP_URL, headers=headers, json=lookup_payload
        )
        data = response.json()

        # 3. Check if status is officially 'Completed'
        if data.get("status") == "Completed":

            # Fetch the order and update
            try:
                order = OrderPlaced.objects.get(
                    id=order_id, transaction_status="Pending"
                )

                # Update Order Status
                order.transaction_status = "Completed"
                order.transaction_id = pidx  # Store the Khalti PIDX as transaction ID
                order.save(update_fields=["transaction_status", "transaction_id"])

                # Clear Cart (PcPeripheralCart) for the user
                if request.user.is_authenticated:
                    PcPeripheralCart.objects.filter(user=request.user).delete()

                # Prepare context for success page
                payment_data = {
                    "payment_method": "Khalti",
                    "order_code": order.order_code,
                    "total_amount": float(order.total_transaction_amount),
                    "transaction_id": str(order.transaction_id),
                }

                return render(
                    request,
                    "MainApps/payment-successfully.html",
                    {"data": payment_data},
                )

            except OrderPlaced.DoesNotExist:
                # If the order is not found or already completed, handle gracefully
                messages.error(request, "Order record not found or already processed.")
                return redirect("home")  # Redirect to home or order history

        else:
            # Payment failed or is still pending/expired
            messages.error(
                request,
                f"Payment verification failed: {data.get('message', 'Transaction status is not Completed.')}",
            )

            # Optional: If you want to delete the pending order on failure:
            try:
                order = OrderPlaced.objects.get(
                    id=order_id, transaction_status="Pending"
                )
                order.delete()
            except OrderPlaced.DoesNotExist:
                pass

            return redirect("cart")

    except requests.exceptions.RequestException:
        messages.error(
            request, "Unable to verify payment status due to a connection error."
        )
        return redirect("cart")


def khalti_payment_success(request):
    """
    Handle Khalti payment success callback.
    Verifies the 'pidx' returned by Khalti.
    """
    # 1. Get Params from URL
    pidx = request.GET.get("pidx")
    order_id = request.GET.get("order_id")

    if not pidx or not order_id:
        messages.error(request, "Invalid payment parameters.")
        return redirect("cart")

    # 2. Verify Payment Status using Khalti Lookup API
    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    lookup_payload = {"pidx": pidx}

    try:
        response = requests.post(
            "https://a.khalti.com/api/v2/epayment/lookup/",
            headers=headers,
            json=lookup_payload,
        )
        data = response.json()

        # 3. Check if status is officially 'Completed'
        if data.get("status") == "Completed":

            # Fetch the order
            try:
                order = OrderPlaced.objects.get(id=order_id)

                # Update Order Status
                order.transaction_status = "Completed"
                order.transaction_id = pidx  # now valid because CharField
                order.save(update_fields=["transaction_status", "transaction_id"])

                # Clear Cart (PcPeripheralCart) for the user
                if request.user.is_authenticated:
                    PcPeripheralCart.objects.filter(user=request.user).delete()

                # Prepare context for success page
                payment_data = {
                    "payment_method": "Khalti",
                    "order_code": order.order_code,
                    "total_amount": float(order.total_transaction_amount),
                    "transaction_id": str(order.transaction_id),
                }

                return render(
                    request,
                    "MainApps/payment-successfully.html",
                    {"data": payment_data},
                )

            except OrderPlaced.DoesNotExist:
                messages.error(request, "Order record not found.")
                return redirect("cart")

        else:
            # Payment failed or is still pending
            messages.error(request, "Payment verification failed or was cancelled.")
            return redirect("cart")

    except requests.exceptions.RequestException:
        messages.error(request, "Unable to verify payment status.")
        return redirect("cart")


def privacy_policy(request):
    return render(request, "MainApps/privacy-policy.html")


from django.shortcuts import render
from django.contrib import messages
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

from .models import NewAdmissionApplication, Certificate, Website
from django.conf import settings

def verify_certificate(request):
    student_data = None
    certificate_obj = None
    certificate_img_url = None

    # Fetch Website config (central template and signatures)
    website = Website.objects.last()
    if not website:
        messages.error(request, "Website configuration not found.")
        return render(request, "MainApps/check-certificate.html")

    if request.method == "POST":
        dob = request.POST.get("dob")
        certificate_number = request.POST.get("certificate_number")

        # Validate both fields
        if not dob or not certificate_number:
            messages.error(request, "Please enter both Date of Birth and Certificate Number.")
            return render(request, "MainApps/check-certificate.html")

        # Fetch certificate directly using certificate number and DOB
        certificate_obj = Certificate.objects.filter(
            certificate_regd_no=certificate_number,
            student_information__date_of_birth=dob
        ).first()

        if not certificate_obj:
            messages.error(request, "No certificate found for the given Date of Birth and Certificate Number.")
            return render(request, "MainApps/check-certificate.html")

        # Certificate exists, fetch student
        student_data = certificate_obj.student_information

        try:
            # Use Website certificate template
            if website.certificate_template and os.path.exists(website.certificate_template.path):
                template_path = website.certificate_template.path
            else:
                messages.error(request, "Website certificate template not found.")
                template_path = None

            if template_path:
                # Open template
                image = Image.open(template_path).convert("RGBA")
                W, H = image.size
                draw = ImageDraw.Draw(image)

                # Load fonts
                font_path = os.path.join(settings.BASE_DIR, "fonts/PlaypenSansDeva.ttf")
                font_student = ImageFont.truetype(font_path, 60) if os.path.exists(font_path) else ImageFont.load_default()
                font_father = font_student
                font_course = ImageFont.truetype(font_path, 80) if os.path.exists(font_path) else ImageFont.load_default()
                font_small = ImageFont.truetype(font_path, 50) if os.path.exists(font_path) else ImageFont.load_default()
                font_watermark = ImageFont.truetype(font_path, 70) if os.path.exists(font_path) else ImageFont.load_default()

                # Draw student info
                student_name = f"{student_data.first_name} {student_data.last_name}"
                bbox = draw.textbbox((0,0), student_name.title(), font=font_student)
                text_w = bbox[2] - bbox[0]
                draw.text(((W - text_w)/5.7, 860), student_name, fill="black", font=font_student)

                father_name = student_data.father_name.title()
                bbox = draw.textbbox((0,0), father_name, font=font_father)
                text_w = bbox[2] - bbox[0]
                draw.text(((W - text_w)/1.30, 865), father_name, fill="black", font=font_father)

                course_name = str(student_data.programs).title()
                bbox = draw.textbbox((0,0), course_name, font=font_course)
                text_w = bbox[2] - bbox[0]
                draw.text(((W - text_w)/2, 1100), course_name, fill="black", font=font_course)

                # Draw dates
                issue_date = certificate_obj.issue_date.strftime("%b %d %Y")
                draw.text((W - 1000, 1350), issue_date, fill="black", font=font_small)
                enroll_date = student_data.booking_date.strftime("%b %d %Y")
                draw.text((W - 2000, 1350), enroll_date, fill="black", font=font_small)
                in_year = student_data.booking_date.strftime(" %Y")
                draw.text((W - 1200, 1440), in_year, fill="black", font=font_small)

                # Helper to paste images
                def paste_image(image_obj, file_field, size, position):
                    if file_field and os.path.exists(file_field.path):
                        img = Image.open(file_field.path).convert("RGBA")
                        img = img.resize(size, resample=Image.Resampling.LANCZOS)
                        image_obj.paste(img, position, img)

                if certificate_obj.is_excutive_head_signature_active:
                    paste_image(image, website.excutive_head_signature_image, (500,350), (W-2500, H-470))
                if certificate_obj.is_shop_stamp_active:
                    paste_image(image, website.shop_stamp_image, (400,400), (W-1820, H-560))
                if certificate_obj.is_course_coodinator_active:
                    paste_image(image, website.course_coodinator, (500,350), (W-1150, H-470))

                # Watermark
                if certificate_obj.is_watermark_active and certificate_obj.watermark_text:
                    watermark_text = certificate_obj.watermark_text
                    watermark_layer = Image.new("RGBA", image.size, (0,0,0,0))
                    watermark_draw = ImageDraw.Draw(watermark_layer)
                    bbox = watermark_draw.textbbox((0,0), watermark_text, font=font_watermark)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x_spacing = text_width + 100
                    y_spacing = text_height + 100
                    for y in range(0, H, y_spacing):
                        for x in range(0, W, x_spacing):
                            watermark_draw.text((x,y), watermark_text, font=font_watermark, fill=(128,128,128,100))
                    watermark_layer = watermark_layer.rotate(30, expand=False)
                    image = Image.alpha_composite(image.convert("RGBA"), watermark_layer)

                # Save certificate
                buffer = BytesIO()
                image = image.convert("RGB")
                filename = f"{student_data.first_name}_{student_data.last_name}_{certificate_obj.certificate_regd_no}.png"

                if certificate_obj.certificate_file and os.path.exists(certificate_obj.certificate_file.path):
                    os.remove(certificate_obj.certificate_file.path)

                image.save(buffer, format="PNG")
                buffer.seek(0)
                certificate_obj.certificate_file.save(filename, ContentFile(buffer.getvalue()), save=True)
                certificate_img_url = certificate_obj.certificate_file.url

                messages.success(request, "Certificate generated successfully.")

        except Exception as e:
            messages.error(request, f"Error generating certificate image: {str(e)}")

    return render(request, "MainApps/check-certificate.html", {
        "student_data": student_data,
        "certificate_obj": certificate_obj,
        "certificate_img_url": certificate_img_url,
    })



def get_client_ip(request):
    """Get client IP address."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


@login_required
def feedback_view(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        comments = request.POST.get("comments")
        source = request.POST.get("shop_institute")  # select field name

        # Validate required fields
        if not rating:
            messages.error(request, "Please provide a rating.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        if not comments or comments.strip() == "":
            messages.error(request, "Please write your feedback in the comments.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        if not source:
            messages.error(request, "Please select Institute or Shop.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # Get user's profile safely
        profile = getattr(request.user, "profile", None)

        # Create Feedback object
        feedback = Feedback(
            user=request.user,
            name=getattr(profile, "full_name", request.user.username),
            email=request.user.email,
            rating=int(rating),
            comments=comments.strip(),
            source=source,
            ip_address=get_client_ip(request),
        )

        # Save profile picture if exists
        if profile and profile.pr_pic:
            feedback.profile_image = profile.pr_pic

        feedback.save()

        messages.success(request, "Thank you! Your feedback has been submitted.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

 
    return render(request, "MainApps/home.html")