"""
Middleware to handle Render health check requests.
Render health checks come from IP addresses, not domain names.
"""

from django.core.exceptions import DisallowedHost
from django.conf import settings
from django.http import HttpResponse


class RenderHealthCheckMiddleware:
    """
    Middleware to bypass ALLOWED_HOSTS check for Render health check requests.
    Health checks from Render use User-Agent "Render/1.0" and come from IP addresses.
    Also handles /health/ endpoint requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if this is a health check request (by path or User-Agent)
        is_health_check = (
            request.path == "/health/" or 
            request.META.get("HTTP_USER_AGENT", "").startswith("Render/")
        )
        
        if is_health_check:
            # Temporarily allow all hosts for health checks
            # This is safe because health checks don't include sensitive headers
            original_allowed_hosts = settings.ALLOWED_HOSTS
            settings.ALLOWED_HOSTS = ["*"]
            
            try:
                response = self.get_response(request)
            except DisallowedHost:
                # If still fails, create a simple 200 response
                response = HttpResponse("OK", status=200, content_type="text/plain")
            finally:
                # Restore original ALLOWED_HOSTS
                settings.ALLOWED_HOSTS = original_allowed_hosts
            
            return response

        return self.get_response(request)
