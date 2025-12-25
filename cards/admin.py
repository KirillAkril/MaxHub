from django.contrib import admin

from .models import PortfolioItem, SocialLink, Testimonial, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "title")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name", "email")}),
        ("Профиль", {"fields": ("title", "bio", "avatar")}),
        ("Разрешения", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важно", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "platform", "label", "url", "order")
    list_filter = ("platform",)
    search_fields = ("user__username", "url")


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "is_published", "created_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "description", "user__username")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "user", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("author_name", "text", "user__username")



