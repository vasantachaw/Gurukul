from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django_ckeditor_5.widgets import CKEditor5Widget

from MainApps.models import (
    Website,
    PcPheripherals,
    PcPeripheralImage,
    PcPeripheralCart,
    Banner,
    Employee,
    AboutUs,
    Blog,
    OrderPlaced,
    OrderItem, ShippingCharge,
    ContactMessage,CourseBooking,Certificate,DigitalService,NewAdmissionApplication,Feedback
)

# ------------------------------
# Website Admin
# ------------------------------

from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'certificate_regd_no',
        'get_student_name',
        'issue_date',
        'is_excutive_head_signature_active',
        'is_shop_stamp_active',
        'is_course_coodinator_active',
        'is_watermark_active',
        'is_available_certificate',
    )

    list_filter = (
        'is_excutive_head_signature_active',
        'is_shop_stamp_active',
        'is_course_coodinator_active',
        'is_watermark_active',
        'is_available_certificate',
        'issue_date',
    )

    search_fields = (
        'certificate_regd_no',
        'student_information__user__username',
        'student_information__full_name',
        'student_information__email',
    )

    readonly_fields = (
        'certificate_regd_no',
        'issue_date',
    )

    ordering = ['-issue_date']

    # Show student's full name in admin list
    def get_student_name(self, obj):
        return obj.student_information.user.username if obj.student_information else "N/A"

    get_student_name.short_description = "Student"




@admin.register(CourseBooking)
class CourseBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'phone','course', 'class_time', 'course_mode', 'booking_date')
    list_filter = ('class_time', 'course_mode', 'booking_date', 'course')
    search_fields = ('user__username', 'course__name', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('-booking_date',)

# ----------------- NewAdmissionApplicationAdmin -----------------
@admin.register(NewAdmissionApplication)
class NewAdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'email', 'phone', 'profile_picture_thumbnail',
        'course_mode_display', 'class_time_display', 'religious_display',
        'student_id', 'date_of_birth'
    )
    list_filter = ('course_mode', 'class_time', 'education_level', 'religious')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'father_name', 'mother_name')
    ordering = ('-booking_date',)

    def course_mode_display(self, obj):
        return obj.get_course_mode_display()
    course_mode_display.short_description = "Course Mode"

    def class_time_display(self, obj):
        return obj.get_class_time_display()
    class_time_display.short_description = "Class Time"

    def religious_display(self, obj):
        return obj.get_religious_display()
    religious_display.short_description = "Religion"

    def profile_picture_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="height:50px; width:auto; border-radius:3px;" />', obj.profile_picture.url)
        return "-"
    profile_picture_thumbnail.short_description = "Profile Picture"

# ----------------- CertificateAdmin -----------------
# 

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_display',
        'rating',
        'source',
        'is_public',
        'created_at',
        'profile_pic_preview',
    )
    
    list_filter = ('source', 'is_public', 'rating', 'created_at')
    search_fields = ('name', 'email', 'comments', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'profile_pic_preview')

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'name', 'email', 'profile_image', 'profile_pic_preview')
        }),
        ('Feedback Details', {
            'fields': ('rating', 'comments', 'source', 'is_public')
        }),
        ('System Info', {
            'fields': ('ip_address', 'created_at', 'updated_at')
        }),
    )

    # 🖼 Thumbnail preview for admin
    def profile_pic_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:8px; object-fit:cover;" />',
                obj.profile_image.url,
            )
        return "No Image"
    profile_pic_preview.short_description = "Profile Image"

    # 👤 Show username or fallback
    def user_display(self, obj):
        if obj.user:
            return obj.user.username  # for custom User model also
        return obj.name or "Guest"
    user_display.short_description = "User"




@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'email', 'phone',
                    'created_at', 'updated_at')
    search_fields = ('name', 'domain', 'email')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25

# ------------------------------
# PcPeripheral Images Inline
# ------------------------------
class PcPeripheralImageInline(admin.TabularInline):
    model = PcPeripheralImage
    extra = 3
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;width:auto;border-radius:5px;" />',
                obj.image.url
            )
        return "No Image"

    preview.short_description = "Preview"


# ------------------------------
# PcPheripherals Admin
# ------------------------------
@admin.register(PcPheripherals)
class PcPheripheralsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'item_type', 'safe_real_price', 'safe_discount_price',
        'is_available', 'stock', 'created_at'
    )
    inlines = [PcPeripheralImageInline]
    readonly_fields = ('created_at', 'updated_at', 'product_code')
    list_filter = ('is_available', 'item_type', 'created_at')
    search_fields = ('name', 'description', 'product_code', 'brand')
    list_per_page = 25
    date_hierarchy = 'created_at'

    def safe_real_price(self, obj):
        try:
            return f"Rs. {float(obj.real_price):.2f}"
        except (TypeError, ValueError):
            return "N/A"
    safe_real_price.short_description = 'Real Price'

    def safe_discount_price(self, obj):
        try:
            return f"Rs. {float(obj.discount_price):.2f}"
        except (TypeError, ValueError):
            return "N/A"
    safe_discount_price.short_description = 'Discount Price'

# ------------------------------
# PcPeripheral Cart Admin
# ------------------------------
@admin.register(PcPeripheralCart)
class PcPeripheralCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'pc_peri', 'quantity', 'total_cost_display')
    search_fields = ('user__username', 'pc_peri__name')
    readonly_fields = ('total_cost_display',)
    list_per_page = 25

    def total_cost_display(self, obj):
        return f"Rs. {obj.total_cost:.2f}"
    total_cost_display.short_description = "Total Cost"

# ------------------------------
# Banner Admin
# ------------------------------
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'is_active',
                    'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;width:auto;border-radius:5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


# ------------------------------
# Employee Admin
# ------------------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('profile_thumb', 'first_name', 'last_name',
                    'email', 'position', 'department', 'hire_date', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'position')
    list_filter = ('position', 'department', 'hire_date', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_per_page = 25

    def profile_thumb(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="height:60px;width:60px;border-radius:50%;" />', obj.profile_image.url)
        return "No Image"
    profile_thumb.short_description = "Profile"


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description", "mission", "vision")
    readonly_fields = ("created_at", "updated_at")

# ------------------------------
# Blog Admin
# ------------------------------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "views", "created_at")
    list_filter = ("is_published", "author", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("views", "created_at", "updated_at")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_code',   # show order code
        'user',         # show user (custom method)
        'peripheral',
        'item_type',
        'quantity',
        'total_cost'
    )
    list_filter = ('item_type',)
    search_fields = ('order__order_code', 'order__user__username', 'peripheral__name')

    readonly_fields = ('id', 'order', 'peripheral', 'item_type', 'quantity', 'total_cost')

    # Order code column
    def order_code(self, obj):
        return obj.order.order_code
    order_code.short_description = "Order Code"

    # User column
    def user(self, obj):
        return obj.order.user.username
    user.short_description = "User"


# OrderPlaced Admin
# ------------------------------
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_code',                 # ✅ Added here
        'user',
        'full_name',
        'payment_method',
        'total_transaction_amount_display',
        'transaction_status',
        'created_at'
    )
    list_filter = ('order_status', 'payment_method')
    search_fields = ('order_code', 'user__username', 'full_name', 'email', 'phone')
    list_per_page = 25
    date_hierarchy = 'created_at'

    def total_transaction_amount_display(self, obj):
        return f"Rs. {obj.total_transaction_amount:.2f}"
    total_transaction_amount_display.short_description = "Total Amount"


@admin.register(ShippingCharge)
class ShippingChargeAdmin(admin.ModelAdmin):
    list_display = (
        'get_location_display',
        'charge',
       
        'carrier_name',
    )
    list_editable = (
        'charge',
       
        'carrier_name',
    )
    search_fields = ('location', 'carrier_name')
    ordering = ('location',)
    list_per_page = 10

    def get_location_display(self, obj):
        return obj.get_location_display()
    get_location_display.short_description = 'Location'







@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')  # Columns to show in list view
    search_fields = ('name', 'email', 'message')    # Search bar fields
    list_filter = ('created_at',)                   # Filter by date
    ordering = ('-created_at',)                     # Latest first








@admin.register(DigitalService)
class DigitalServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')