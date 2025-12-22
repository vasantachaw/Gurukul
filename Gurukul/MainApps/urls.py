from django.urls import path
from MainApps import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = "𝗚𝘂𝗿𝘂𝗸𝘂𝗹 𝗜𝗧 𝗣𝗹𝗮𝘇𝗮 𝗔𝗱𝗺𝗶𝗻"
admin.site.site_title = "𝗚𝘂𝗿𝘂𝗸𝘂𝗹 𝗜𝗧 𝗣𝗹𝗮𝘇𝗮 𝗔𝗱𝗺𝗶𝗻 𝗣𝗼𝗿𝘁𝗮𝗹"
admin.site.index_title = "𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗚𝘂𝗿𝘂𝗸𝘂𝗹 𝗜𝗧 𝗣𝗹𝗮𝘇𝗮 𝗔𝗱𝗺𝗶𝗻 𝗣𝗼𝗿𝘁𝗮𝗹"

urlpatterns = [
    path("", views.home, name="home"),
    path("product-list/", views.ProductList, name="productList"),
    path("course-list/", views.CourseList, name="courseList"),
    path("pc-product-view/<int:pk>/", views.Pc_ProductView, name="Pc_ProductView"),
    path("buy-now/<int:pk>/", views.buy_now, name="buy_now"),
    # PC cart URLs
    path("pc/add-to-cart/<int:pc_id>/", views.add_pc_to_cart, name="add_pc_to_cart"),
    path("cart/plus/", views.plus_pc_cart, name="plus_pc_cart"),
    path("cart/minus/", views.minus_pc_cart, name="minus_pc_cart"),
    path("cart/remove/<int:pk>/", views.remove_pc_from_cart, name="remove_pc_cart"),
    path("blog/<int:pk>/", views.BlogDetailView, name="blog_detail"),
    path("checkout/", views.CheckOut, name="checkout"),
    path("checkout/place-order/", views.place_order, name="place_order"),
    path("cart/", views.show_cart, name="cart"),
    path(
        "shipping-delivery-info/",
        views.shipping_and_delivery_info,
        name="shipping_and_delivery_info",
    ),
    path("gallery/", views.Bloglist, name="gallery"),
    path("contact-us/", views.contact_view, name="contact"),
    path("search/", views.search_query, name="search_query"),
    path("about-us/", views.about_us, name="about_us"),
    path("course-booking/", views.courseBooking, name="course_booking"),
    # path("certificate/image/", views.certificateGenerate, name="certificate"),
    # path("payment/khalti/", views.khalti_payment, name="khalti_payment"), # <-- OLD/REDUNDANT PATH
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),

    path("service-pricing/", views.service_pricing, name="service_pricing"),
    path("admin-orders/", views.admin_orders, name="admin_orders"),
    path("invoice/<int:order_id>/", views.invoice_view, name="generate_invoice"),
    path(
        "payment/payment-confirmation/",
        views.cod_confirmation,
        name="payment_confirmation_with_cod",
    ),
    # --- eSewa Payment Routes ---
    path(
        "payment/payment-confirmation-esewa/", views.esewa_payment_view, name="payment_confirm_with_esewa"
    ),
    path("payment/esewa/success/", views.esewa_payment_success, name="esewa_success"),
    # path("payment-success/", views.esewa_payment_success, name="payment_success"), # <-- REDUNDANT/CONFUSING PATH

    # --- Khalti Payment Routes (New/Corrected) ---
    path(
        "payment/payment-confirmation-khalti/", 
        views.khalti_confirm, 
        name="payment_confirm_with_khalti"
    ),
    path("payment/khalti/", views.khalti_payment_view, name="khalti_payment"),
    path(
        "payment/khalti/success/", 
        views.khalti_payment_success, 
        name="khalti_success"
    ),
    
    # --- Other Payment/Utility Routes ---
    path("payment/methods/", views.payment_methods, name="payment_methods"),
    path("payment/cod/", views.cod_payment, name="cash_on_delivery"),
    path("payment/paypal/", views.paypal_payment, name="paypal_payment"),
    path("payment/success/", views.payment_successful, name="payment_successful"),
    path("payment/cash-on-delivery/success/<int:order_id>/", views.cod_success, name="cod_success"),
    path('check-certificate-status/',views.check_certificate_status,name='check_certificate'),
    path('new-admission-form/',views.new_admission_applications,name='new_admission_form'),
    path('verify-certificate/',views.verify_certificate,name='verify_certificate'),
    path('client-feedbacks/',views.feedback_view,name='feedback'),

    #path("payment-failure/", views.esewa_payment_failure, name="payment_failure"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)