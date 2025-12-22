from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.dispatch import receiver
from django.core.files.base import ContentFile
from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.contrib import messages
import requests
import os

class Profile(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    ph_num = models.CharField(max_length=10, blank=True)
    pr_pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='OTHER')
    website = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.ph_num or 'N/A'}"

    def get_contact_info(self):
        return f"Email: {self.user.email}, Phone: {self.ph_num or 'N/A'}"

    def get_profile_picture_url(self):
        if self.pr_pic:
            return self.pr_pic.url
        return static('default_profile_pic.jpg')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']



def create_or_update_profile(user, socialaccount=None, request=None):
    """
    Create or update a Profile object for the given user.

    - If `socialaccount` is provided, extract full_name, profile picture, and email from it.
    - Avoid overwriting existing profile data unnecessarily.
    - Optionally, send success messages via Django messages framework.
    """
    profile, created = Profile.objects.get_or_create(user=user)
    updated = False

    if socialaccount:
        extra_data = socialaccount.extra_data

        # Full name from social account
        full_name = extra_data.get("name") or extra_data.get("full_name")
        if full_name and full_name != profile.full_name:
            profile.full_name = full_name
            updated = True

        # Profile picture from social account
        profile_pic_url = (
            extra_data.get("picture")
            or extra_data.get("profile_picture")
            or extra_data.get("avatar_url")
        )
        if profile_pic_url and not profile.pr_pic:
            try:
                response = requests.get(profile_pic_url)
                if response.status_code == 200:
                    file_name = os.path.basename(profile_pic_url.split("?")[0])
                    profile.pr_pic.save(file_name, ContentFile(response.content), save=False)
                    updated = True
            except Exception as e:
                print(f"Failed to download profile picture: {e}")

        # Update user email if empty
        if extra_data.get("email") and not user.email:
            user.email = extra_data.get("email")
            user.save()
            updated = True

    profile.save()

    # Optional success messages
    if request:
        if created:
            messages.success(request, "Profile created successfully!")
        elif updated:
            messages.success(request, "Profile updated successfully!")
class MerchantAccount(models.Model):
    GATEWAY_CHOICES = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
    ]

    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES)
    merchant_id = models.CharField(max_length=100, help_text="Your merchant ID or public key")
    secret_key = models.CharField(max_length=200, help_text="Your secret key or API key")
    environment = models.CharField(
        max_length=20,
        choices=[('sandbox', 'Sandbox/Test'), ('production', 'Production')],
        default='sandbox'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('gateway', 'environment')
        verbose_name = "Merchant Account"
        verbose_name_plural = "Merchant Accounts"

    def __str__(self):
        return f"{self.gateway.upper()} ({self.environment})"




# -----------------------------
# Signals
# -----------------------------
@receiver(user_signed_up)
def handle_user_signed_up(sender, request, user, **kwargs):
    socialaccount = user.socialaccount_set.first()
    create_or_update_profile(user, socialaccount, request=request)


@receiver(social_account_added)
def handle_social_account_added(sender, request, sociallogin, **kwargs):
    create_or_update_profile(sociallogin.user, sociallogin.account, request=request)


@receiver(social_account_updated)
def handle_social_account_updated(sender, request, sociallogin, **kwargs):
    create_or_update_profile(sociallogin.user, sociallogin.account, request=request)


@receiver(user_logged_in)
def show_login_message(sender, request, user, **kwargs):
    messages.success(request, f"Welcome back, {user.username}!")
