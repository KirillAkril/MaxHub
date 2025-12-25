from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


def upload_to_avatar(instance, filename):
    return f"avatars/{instance.username}/{filename}"


def upload_to_portfolio(instance, filename):
    return f"portfolio/{instance.user.username}/{filename}"


def upload_to_testimonial(instance, filename):
    return f"testimonials/{instance.user.username}/{filename}"


class User(AbstractUser):
    title = models.CharField("Заголовок/роль", max_length=150, blank=True)
    bio = models.TextField("Биография", blank=True)
    avatar = models.ImageField("Аватар", upload_to=upload_to_avatar, blank=True, null=True)
    max_username = models.CharField("Username аккаунта в MAX", max_length=150, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("phone", "Телефон"),
        ("email", "Email"),
        ("telegram", "Telegram"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("website", "Website"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField("Платформа", max_length=50, choices=PLATFORM_CHOICES)
    label = models.CharField("Подпись", max_length=100, blank=True)
    url = models.CharField("Значение/URL", max_length=255)
    icon = models.CharField("Иконка (class)", max_length=100, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Социальная ссылка"
        verbose_name_plural = "Социальные ссылки"

    def __str__(self):
        return f"{self.user.username} - {self.platform}"


class PortfolioItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolio_items")
    title = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to=upload_to_portfolio, blank=True, null=True)
    project_archive = models.FileField(
        "Архив проекта (zip)", upload_to=upload_to_portfolio, blank=True, null=True
    )
    category = models.CharField("Категория", max_length=100, blank=True)
    created_at = models.DateField("Дата", default=timezone.now, blank=True)
    is_published = models.BooleanField("Публиковать", default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Проект портфолио"
        verbose_name_plural = "Проекты портфолио"

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="testimonials")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_testimonials",
        verbose_name="Автор отзыва",
    )
    author_name = models.CharField("Автор", max_length=150)
    author_title = models.CharField("Должность/роль", max_length=150, blank=True)
    text = models.TextField("Текст отзыва")
    is_published = models.BooleanField("Публиковать", default=True)
    created_at = models.DateField("Дата", default=timezone.now, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.author_name} -> {self.user.username}"

