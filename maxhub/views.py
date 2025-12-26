"""
Simple views for health check and other utilities.
"""
from django.http import HttpResponse


def health_check(request):
    """
    Simple health check endpoint that always returns 200 OK.
    This endpoint doesn't require ALLOWED_HOSTS validation.
    Used by Render for service health monitoring.
    """
    return HttpResponse("OK", status=200, content_type="text/plain")

