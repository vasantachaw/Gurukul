from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Authentications import views

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('my-account/',views.myaccount,name='myaccount'),
    path('my-orders/',views.orders,name='myorder'),
    path('my-address/', views.address, name='myaddress'),
    path('edit-address/',views.editAdress,name="edit_address"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='user_login'),
     path("update-profile/", views.update_profile, name="update_profile"),
     path('edit-password/',views.editPassword,name="edit_password"),
     path('change-password/', views.change_password, name='change_password'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
