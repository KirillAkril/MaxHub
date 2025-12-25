from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cards.urls")),  # Включаем первым, чтобы кастомный login имел приоритет
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", include("cards.dashboard_urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


