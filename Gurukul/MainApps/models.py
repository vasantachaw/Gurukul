import uuid
import random
import string
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# ------------------------------
# Utility Functions
# ------------------------------
def generate_unique_code(model_class, field_name="product_code", length=6):
    """
    Generates a unique alphanumeric code for the given model.
    :param model_class: Django model class
    :param field_name: Field name to check uniqueness
    :param length: Length of the code
    :return: Unique code string
    """
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        filter_kwargs = {field_name: code}
        if not model_class.objects.filter(**filter_kwargs).exists():
            return code

# ------------------------------
# Website Models
# ------------------------------
class Website(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, unique=True)
    description = CKEditor5Field(blank=True)
    logo1 = models.ImageField(upload_to="website_logos/", blank=True, null=True)
    logo2 = models.ImageField(upload_to="website_logos/", blank=True, null=True)
    favicon = models.ImageField(upload_to="website_logos/", blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pan_no = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    # Social Links & Apps
    android_app = models.FileField(upload_to="apps/android/", blank=True, null=True,
                                   help_text="Upload your Android APK file.")
    desktop_app = models.FileField(upload_to="apps/desktop/", blank=True, null=True,
                                   help_text="Upload your Desktop application file.")
    ios_app = models.FileField(upload_to="apps/ios/", blank=True, null=True,
                               help_text="Upload your iOS IPA file.")
    
    certificate_template = models.FileField(upload_to='certificate_template/', blank=True, null=True)
    excutive_head_signature_image = models.FileField(upload_to='executive_head_signature/',blank=True,null=True)
    shop_stamp_image = models.FileField(upload_to='shop_stamp/',blank=True,null=True)
    # Course Coordinator Signature
    course_coodinator = models.FileField(
        upload_to='course_coordinator/',
        blank=True,
        null=True
    )

    fb = models.URLField(blank=True, null=True)
    insta = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    snapchat = models.URLField(blank=True, null=True)
    reddit = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    discord = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_full_domain(self):
        return f"https://{self.domain}"

    @staticmethod
    def get_current_site():
        return Site.objects.get_current().domain


class WebsiteBanner(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="banners")
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="website_banners/")
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.website.name}"

    class Meta:
        verbose_name = "Website Banner"
        verbose_name_plural = "Website Banners"
        ordering = ["-created_at"]

# ------------------------------
# PC Peripherals & Courses
# ------------------------------
class PcPheripherals(models.Model):
    # Choice Groups
    INPUT_DEVICES = [
        ("keyboard", "Keyboard"),
        ("mouse", "Mouse"),
        ("scanner", "Scanner"),
        ("joystick", "Joystick/Game Controller"),
        ("graphics_tablet", "Graphics/Tablet"),
        ("trackball", "Trackball"),
        ("drawing_pad", "Drawing Pad"),
        ("touchscreen", "Touchscreen"),
        ("barcode_scanner", "Barcode Scanner"),
    ]
    OUTPUT_DEVICES = [
        ("monitor", "Monitor"),
        ("printer", "Printer"),
        ("speakers", "Speakers/Headphones"),
        ("projector", "Projector/VR Display"),
    ]
    STORAGE_DEVICES = [
        ("hdd", "HDD"),
        ("ssd", "SSD"),
        ("usb_flash_drive", "USB Flash Drive"),
        ("sd_card", "SD Card"),
        ("network_storage", "NAS/Cloud Storage"),
        ("optical_drive", "CD/DVD/Blu-ray Drive"),
    ]
    NETWORK_DEVICES = [
        ("network_adapter", "Network Adapter"),
        ("router", "Router/Switch/Access Point"),
        ("modem", "Modem"),
        ("firewall", "Firewall"),
    ]
    COMPUTING_DEVICES = [
        ("laptop", "Laptop"),
        ("desktop_pc", "Desktop PC"),
        ("server", "Server"),
        ("smartphone", "Smartphone/Tablet"),
        ("workstation", "Workstation/Thin Client"),
    ]
    OTHER = [
        ("webcam", "Webcam"),
        ("headset", "Headset/Microphone"),
        ("vr_headset", "VR Headset"),
        ("graphics_card", "Graphics Card"),
        ("sound_card", "Sound Card"),
        ("power_supply", "Power Supply"),
        ("cooling_fan", "Cooling Fan"),
        ("pc_case", "PC Case"),
        ("motherboard", "Motherboard"),
        ("processor", "CPU"),
        ("ram", "RAM"),
        ("ethernet_cable", "Ethernet Cable"),
        ("vga_cable", "VGA Cable"),
        ("hdmi_cable", "HDMI Cable"),
        ("usb_cable", "USB/Data Cable"),
        ("usb_typec_cable", "USB Type-C Cable"),
        ("power_cable", "Power Cable"),
        ("audio_cable", "Audio Cable"),
        ("displayport_cable", "DisplayPort Cable"),
        ("dvi_cable", "DVI Cable"),
        ("adapter", "Adapters (HDMI/USB/etc.)"),
        ("extension_cable", "Extension Cable"),
        ("other", "Other"),
    ]
    DEVICE_TYPES = INPUT_DEVICES + OUTPUT_DEVICES + STORAGE_DEVICES + NETWORK_DEVICES + COMPUTING_DEVICES + OTHER

    FOR_CHOICES = [("Trending", "Trending"), ("Best", "Best")]
    ITEM_TYPE_CHOICES = [("device", "Device"), ("course", "Course")]

    # Common Fields
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    description = CKEditor5Field(blank=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    product_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    for_type = models.CharField(max_length=100, choices=FOR_CHOICES, default="Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Device Fields
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES, blank=True, null=True)
    real_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    warranty_period = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)

    # Course Fields
    instructor_name = models.CharField(max_length=100, blank=True, null=True)
    course_duration = models.CharField(max_length=100, blank=True, null=True)
    course_level = models.CharField(
        max_length=50,
        choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")],
        blank=True, null=True
    )
    course_language = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    enrollment_limit = models.PositiveIntegerField(blank=True, null=True)
    pdf_file = models.FileField(upload_to="pc_peripherals/pdfs/", blank=True, null=True)
    certificate_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    


class PcPeripheralImage(models.Model):
    peripheral = models.ForeignKey(PcPheripherals, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="pc_peripherals/")

    def __str__(self):
        return f"{self.peripheral.name} Image"


# ------------------------------
# General Banners
# ------------------------------
class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="banners/")
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ["-created_at"]

# ------------------------------
# Employee Model
# ------------------------------
class Employee(models.Model):
    DEPARTMENT_CHOICES = [("Trainer", "Trainer"), ("Technician", "Technician"), ("Developer", "Developer"), ("Other", "Other")]
    POSITION_CHOICES = [("Admin", "Admin"), ("Employee", "Employee")]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to="employee_profiles/", blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    about = CKEditor5Field(blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    twitter = models.URLField(max_length=200, blank=True)
    github = models.URLField(max_length=200, blank=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# ------------------------------
# Course Models
# ------------------------------
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field(blank=True)
    course_banner = models.ImageField(upload_to="course_banners/")
    instructor = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    real_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    views = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    course_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.course_code:
            self.course_code = generate_unique_code(Course, "course_code", 6)
        super().save(*args, **kwargs)


class CourseCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_c = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CourseCart #{self.id}"

    @property
    def total_cost(self):
        return self.quantity * self.course_c.discount_price


class CourseBooking(models.Model):
    
    CLASS_TIME_CHOICES = [
        ('morning', 'Morning'),
        ('evening', 'Evening'),
    ]
    COURSE_MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    course=models.CharField( max_length=50)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    models.EmailField(unique=True)
    phone=models.CharField(max_length=100)
    class_time = models.CharField(max_length=20, choices=CLASS_TIME_CHOICES, default='morning')
    course_mode = models.CharField(max_length=20, choices=COURSE_MODE_CHOICES, default='offline')
    note = models.TextField(blank=True, null=True)

    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.course}"


# ------------------------------
# Blog Model
# ------------------------------
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to="Blogs/thumbnails/", blank=True, null=True)
    video = models.FileField(upload_to="Blogs/videos/", blank=True, null=True)
    content = CKEditor5Field()
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

# ------------------------------
# PC Peripheral Cart
# ------------------------------
class PcPeripheralCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pc_peri = models.ForeignKey(PcPheripherals, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart Item #{self.id}"

    @property
    def total_cost(self):
        return self.quantity * self.pc_peri.discount_price

# ------------------------------
# Order Models
# ------------------------------

class OrderPlaced(models.Model):
    ORDER_STATUS = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]
    PAYMENT_METHODS = [
        ("cod", "Cash on Delivery"),
        ("bank", "Bank Transfer"),
        ("esewa", "eSewa"),
        ("khalti", "Khalti"),
        ("paypal", "PayPal"),
        ('imepay','imepay'),
    ]

    # New custom order ID
    order_code = models.CharField(max_length=12, unique=True, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default="Pending")
    transaction_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default="Pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="cod")
    note = models.TextField(blank=True, null=True)
    total_transaction_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_code} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = self.generate_order_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_code():
        """Generate random 6-character mixed alphanumeric code"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def update_total_amount(self):
        total = sum(item.total_cost for item in self.items.all())
        self.total_transaction_amount = total
        self.save()


class OrderItem(models.Model):
    ITEM_TYPES = [
        ("device", "Device"),
        ("course", "Course"),
    ]

    order = models.ForeignKey(OrderPlaced, on_delete=models.CASCADE, related_name="items")
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    peripheral = models.ForeignKey(PcPheripherals, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        user = getattr(self.order, "user", None)

        if user:
            username = getattr(user, "username", None)
            name_display = username if username else getattr(user, "first_name", "")
        else:
            name_display = "Unknown User"

        # Use custom order code instead of order.id
        order_code = getattr(self.order, "order_code", "NOCODE")

        return f"{name_display} - {self.item_type}"

    @property
    def total_cost(self):
        return self.quantity * self.peripheral.discount_price


class ShippingCharge(models.Model):
    LOCATION_CHOICES = [
        ("in_valley", "Inside Valley"),
        ("out_valley", "Outside Valley"),
        ("international", "International"),
        ("remote_area", "Remote Area"),
    ]

    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, unique=True, verbose_name="Delivery Location")
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                 validators=[MinValueValidator(0)], verbose_name="Shipping Charge (Rs)")
    carrier_name = models.CharField(max_length=100, default="Daraz Express",
                                    help_text="Name of the shipping carrier (e.g., UPS Express).")
    product_return_in_days = models.PositiveIntegerField(default=0,
                                                         help_text="Number of days allowed for product returns.")

    class Meta:
        verbose_name = "Shipping Charge"
        verbose_name_plural = "Shipping Charges"
        ordering = ["location"]

    def __str__(self):
        return f"{self.get_location_display()} - Rs {self.charge:.2f}"

    def get_shipping_note(self):
        return (
            f"All orders are shipped via {self.carrier_name}. "
            f"Shipping charge for {self.get_location_display()} is Rs {self.charge:.2f}. "
            f"Products can be returned within {int(self.product_return_in_days)} days."
        )

# ------------------------------
# Contact & About Us
# ------------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} <{self.email}>"


class AboutUs(models.Model):
    SECTION_CHOICES = [
        ("gurukul", "Our Gurukul"),
        ("vision", "Our Vision"),
        ("mission", "Our Mission"),
        ("software", "Software Development"),
        ("hardware_lab", "Computer Repair, Hardware & IT Support Lab"),
        ("computer_lab", "Modern Computer Lab"),
        ("study_env", "Study Environment"),
        ("established", "Established since ..."),
    ]

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=SECTION_CHOICES, default="gurukul")
    description = models.TextField(help_text="Main content for the About Us section.")
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="about_us/images/", blank=True, null=True)
    video = models.FileField(upload_to="about_us/videos/", blank=True, null=True,
                             help_text="Upload intro or promotional video.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us Sections"

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"

class DigitalService(models.Model):
    DIGITAL_SOLUTIONS = (
        ('WEB_DEVELOPMENT', 'Web Development'),
        ('WINDOWS_SOFTWARE', 'Windows Software Development'),
        ('MOBILE_APP', 'Mobile App Development'),
        ('MARKETING', 'Marketing & SEO'),
        ('DIGITAL_DESIGN', 'Digital Design & UI/UX'),
        ('SEO_SERVICES', 'Search Engine Optimization'),
        ('CONTENT_CREATION', 'Content Creation & Copywriting'),
        ('SOCIAL_MEDIA', 'Social Media Management'),
        ('CLOUD_SERVICES', 'Cloud & Hosting Services'),
        ('DATA_ANALYTICS', 'Data Analytics & BI'),
        ('IT_SUPPORT', 'IT Support & Maintenance'),
        ('VIDEO_PRODUCTION', 'Video Production & Editing'),
        ('DIGITAL_MARKETING', 'Digital Marketing Strategy'),
       
    )

    name = models.CharField(max_length=150)
    description = CKEditor5Field(blank=True, null=True)
    category = models.CharField(max_length=100, choices=DIGITAL_SOLUTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name
    

# ----------------- Utility Functions -----------------
def generate_unique_code(model_class, field_name="certificate_no", length=6):
    """Generate a unique alphanumeric code for certificates."""
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not model_class.objects.filter(**{field_name: code}).exists():
            return code


# ----------------- NewAdmissionApplication -----------------
class NewAdmissionApplication(models.Model):
    GENDER_CHOICES = [('MALE', 'Male'), ('FEMALE', 'Female')]
    CLASS_TIME_CHOICES = [('MORNING', 'Morning'), ('AFTERNOON', 'Afternoon'), ('EVENING', 'Evening')]
    COURSE_MODE_CHOICES = [('OFFLINE', 'Offline'), ('ONLINE', 'Online')]
    EDUCATION_LEVEL_CHOICES = [('HIGH_SCHOOL', 'High School'), ('INTERMEDIATE', 'Intermediate'),
                               ('BACHELOR', 'Bachelor'), ('MASTER', 'Master'), ('OTHER', 'Other')]
    RELIGION_CHOICES = [('HINDU', 'Hindu'), ('BUDDHIST', 'Buddhist'), ('MUSLIM', 'Muslim'),
                        ('CHRISTIAN', 'Christian'), ('OTHER', 'Other')]

    # User Info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admissions')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='admissions/profile_pictures/', blank=True, null=True)
    phone = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    # Family Info
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    local_parents_name = models.CharField(max_length=100, blank=True, null=True)
    local_parents_number = models.CharField(max_length=100, blank=True, null=True)
    religious = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True, null=True)

    # Address
    address_street = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    zip_postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, default='Nepal')

    # Education & Course
    programs = models.CharField(max_length=50, blank=True, null=True)
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES, blank=True, null=True)
    school_college_name = models.CharField(max_length=255, blank=True, null=True)
    class_time = models.CharField(max_length=20, choices=CLASS_TIME_CHOICES, default='MORNING')
    course_mode = models.CharField(max_length=20, choices=COURSE_MODE_CHOICES, default='OFFLINE')

    # Other fields
    note = models.TextField(blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    # Auto generation
    student_id = models.CharField(max_length=255, blank=True, null=True)

    def generate_student_id(self):
        last_record = NewAdmissionApplication.objects.order_by('-id').first()
        if last_record and last_record.student_id and last_record.student_id.isdigit():
            return str(int(last_record.student_id) + 1).zfill(4)
        return "0001"

   

    class Meta:
        ordering = ['-booking_date']
        constraints = [
            models.UniqueConstraint(fields=['user', 'email'], name='unique_user_email')
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.date_of_birth})"

class Certificate(models.Model):
    student_information = models.ForeignKey(
        'NewAdmissionApplication',
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    issue_date = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    # Executive Head Signature
    
    is_excutive_head_signature_active = models.BooleanField(
        default=False,
        verbose_name="Active Executive Head Signature"
    )

    # Shop Stamp
    
    is_shop_stamp_active = models.BooleanField(
        default=False,
        verbose_name="Active Shop Stamp"
    )
  
    is_course_coodinator_active = models.BooleanField(
        default=False,
        verbose_name="Active Course Coordinator Signature"
    )

    # Watermark
    watermark_text = models.CharField(
        max_length=50,
        default="OFFICIAL",
        blank=True,
        null=True
    )
    is_watermark_active = models.BooleanField(
        default=True,
        verbose_name="Active Watermark"
    )
    certificate_regd_no = models.CharField(max_length=6, unique=True, blank=True, editable=True)
    is_available_certificate = models.BooleanField(default=False)

    class Meta:
        ordering = ['-issue_date']

    def save(self, *args, **kwargs):
        if not self.certificate_regd_no:
            self.certificate_regd_no = generate_unique_code(Certificate, "certificate_regd_no", 6)
        super().save(*args, **kwargs)

    def __str__(self):
        username = getattr(self.student_information.user, 'username', 'N/A')
        return f"{username}"




class Feedback(models.Model):
    SOURCE_CHOICES = [
        ('institute', 'Institute'),
        ('shop', 'Shop'),
        ('both', 'Institute & Shop'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feedbacks'
    )
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)

    # ⭐ Store user photo for public feedback
    profile_image = models.ImageField(
        upload_to='feedback_profile/',
        blank=True,
        null=True
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comments = models.TextField()
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='both')
    is_public = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        who = self.name or (self.user.get_full_name() if self.user else 'Anonymous')
        return f'{who} — {self.rating} ★ — {self.created_at:%Y-%m-%d %H:%M}'
