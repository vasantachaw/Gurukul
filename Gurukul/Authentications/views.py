from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Authentications.models import Profile
from MainApps import models


# ------------------------------
# Logout View
# ------------------------------
def logout_view(request):
    logout(request)
    return redirect("/")


# ------------------------------
# My Account
# ------------------------------
def myaccount(request):
    return render(request, "MainApps/my-account.html")


# ------------------------------
# Orders View
# ------------------------------
def orders(request):
    user_orders = models.OrderPlaced.objects.filter(user=request.user).prefetch_related(
        "items__peripheral"
    )
    context = {"orders": user_orders}
    return render(request, "MainApps/my-account-orders.html", context)


def address(request):
    profile = Profile.objects.filter(user=request.user).first()
    context = {"profile": profile}
    return render(request, "MainApps/my-account-address.html", context)


def editAdress(request):
    return render(request, "MainApps/my-account-edit-address.html")


def editPassword(request):
    return render(request, "MainApps/my-account-edit.html")


# ------------------------------
# Registration (AJAX)
# ------------------------------
def register(request):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        errors = []

        # Validate
        if not all(
            [first_name, last_name, username, email, password, confirm_password]
        ):
            errors.append("All fields are required.")
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username is already taken.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered.")
        if email and "@" not in email:
            errors.append("Please enter a valid email address.")

        if errors:
            return JsonResponse({"success": False, "messages": errors})

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        Profile.objects.create(user=user, full_name=f"{first_name} {last_name}")

        # Auto-login
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse(
                {"success": True, "messages": ["Registration successful!"]}
            )
        else:
            return JsonResponse({"success": False, "messages": ["Error logging in."]})

    return JsonResponse({"success": False, "messages": ["Invalid request."]})


# ------------------------------
# Login View (Username or Email)
# ------------------------------
def login_view(request):
    if request.method == "POST":
        login_input = request.POST.get(
            "email", ""
        ).strip()  # could be username or email
        password = request.POST.get("password", "")

        # First, check if user exists by username or email
        user_exists = (
            User.objects.filter(username=login_input).exists()
            or User.objects.filter(email=login_input).exists()
        )

        if not user_exists:
            messages.error(
                request, "User is not registered. Please create an account first."
            )
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # Try login by username first
        user = authenticate(request, username=login_input, password=password)

        # If not found, try login by email
        if user is None:
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(
                    request, username=user_obj.username, password=password
                )
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            messages.success(
                request, f"Welcome back, {user.first_name or user.username}!"
            )
        else:
            messages.error(request, "Invalid password. Please try again.")

        return redirect(request.META.get("HTTP_REFERER", "/"))

    return redirect("/")


@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update User model fields
        user.username = request.POST.get("username", user.username)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()

        # Update Profile model fields
        profile.full_name = (
            f"{user.first_name} {user.last_name}".strip() or profile.full_name
        )
        profile.ph_num = request.POST.get("ph_num", profile.ph_num)
        profile.bio = request.POST.get("bio", profile.bio)
        profile.address = request.POST.get("address", profile.address)
        profile.city = request.POST.get("city", profile.city)
        profile.gender = request.POST.get("gender", profile.gender)
        profile.dob = request.POST.get("dob", profile.dob)

        if "pr_pic" in request.FILES:
            profile.pr_pic = request.FILES["pr_pic"]

        profile.save()

        return JsonResponse(
            {"success": True, "message": "Profile updated successfully!"}
        )

    return JsonResponse({"success": False, "message": "Invalid request method."})


@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            return JsonResponse(
                {"status": "error", "message": "Current password is incorrect."}
            )

        if new_password != confirm_password:
            return JsonResponse(
                {"status": "error", "message": "Passwords do not match."}
            )

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keep user logged in
        return JsonResponse(
            {"status": "success", "message": "Password changed successfully."}
        )

    return JsonResponse({"status": "error", "message": "Invalid request method."})
