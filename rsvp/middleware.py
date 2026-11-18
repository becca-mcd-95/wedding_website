from django.shortcuts import redirect
from django.urls import reverse

class SitePasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__ (self, request):
        if request.path == reverse("site_password") or request.path.startswith("/admin/") or request.path.startswith("/static/"):
            return self.get_response(request)

        if request.session.get("site_unlocked"):
            return self.get_response(request)
        
        return redirect("site_password")