# restrict_middleware.py

from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, Resolver404
import re

class AccessRestrictionMiddleware:
    """Restricts access to all URLs unless whitelisted or user is authenticated."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = list(settings.PUBLIC_URLS)
        
        # Regex for views that take primary keys (e.g., /pc-product-view/12/)
        # We assume public detail views follow the /path/<int:pk>/ pattern.
        self.public_regexes = [
            re.compile(r'^/pc-product-view/\d+/$'),
            re.compile(r'^/blog/\d+/$'),
        ]

    def __call__(self, request):
        current_path = request.path_info
        
        # 1. Check if the user is authenticated (allowed access to everything)
        if request.user.is_authenticated:
            return self.get_response(request)

        # 2. Check if the exact path is explicitly whitelisted
        if current_path in self.public_paths:
            return self.get_response(request)

        # 3. Check if the path matches a whitelisted regex (for detail views)
        for regex in self.public_regexes:
            if regex.match(current_path):
                return self.get_response(request)

        # 4. Deny access and redirect to login page
        # This will block URLs like /checkout/, /cart/, /admin-orders/, /invoice/12, etc.
        return redirect(settings.LOGIN_URL)