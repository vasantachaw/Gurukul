from django.contrib import admin
from .models import Profile,MerchantAccount
from django.utils.html import format_html

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'full_name',
        'ph_num',
        'gender',
        'get_profile_pic_preview',
        'created_at',
        'updated_at',
    )
    list_filter = ('gender', 'created_at')
    search_fields = ('user__username', 'full_name', 'ph_num', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'get_profile_pic_preview')
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'ph_num', 'gender', 'dob', 'website', 'bio', 'address', 'city')
        }),
        ('Profile Picture', {
            'fields': ('pr_pic', 'get_profile_pic_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_profile_pic_preview(self, obj):
        if obj.pr_pic:
            return format_html('<img src="{}" style="height:60px;width:60px;border-radius:50%;" />', obj.pr_pic.url)
        return "(No Image)"
    get_profile_pic_preview.short_description = 'Profile Picture Preview'





@admin.register(MerchantAccount)
class MerchantAccountAdmin(admin.ModelAdmin):
    list_display = ('gateway', 'environment', 'merchant_id', 'is_active', 'updated_at')
    list_filter = ('gateway', 'environment', 'is_active')
    search_fields = ('merchant_id', 'gateway')