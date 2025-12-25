from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from django.contrib.auth.views import LoginView as DjangoLoginView

from .forms import LoginForm, PortfolioItemForm, ProfileForm, SignupForm, SocialLinkForm, TestimonialForm
from .models import PortfolioItem, SocialLink, Testimonial, User


class HomeView(TemplateView):
    template_name = "home.html"


class CustomLoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "registration/login.html"


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def get_success_url(self):
        return reverse("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        # Автовход после регистрации
        from django.contrib.auth import login

        login(self.request, user)
        return response


class CardDetailView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "public/card_detail.html"
    context_object_name = "card_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card_user = self.object
        context["social_links"] = card_user.social_links.all()
        context["portfolio_items"] = card_user.portfolio_items.filter(is_published=True)
        context["testimonials"] = card_user.testimonials.filter(is_published=True)
        return context


class UserSearchView(ListView):
    model = User
    template_name = "public/user_search.html"
    context_object_name = "users"

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return User.objects.none()
        return User.objects.filter(Q(username__icontains=q)).order_by("username")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["portfolio_count"] = user.portfolio_items.count()
        context["testimonials_count"] = user.testimonials.count()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "dashboard/profile_form.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.instance
        # удаление аватара отдельной кнопкой
        if "remove_avatar" in self.request.POST:
            if user.avatar:
                user.avatar.delete(save=False)
            user.avatar = None
        messages.success(self.request, "Профиль сохранён.")
        return super().form_valid(form)


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class SocialLinkListView(LoginRequiredMixin, ListView):
    model = SocialLink
    template_name = "dashboard/social_links.html"

    def get_queryset(self):
        return self.request.user.social_links.all()


class SocialLinkCreateView(LoginRequiredMixin, CreateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("social_links")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Ссылка сохранена.")
        return super().form_valid(form)


class SocialLinkUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("social_links")


class PortfolioListView(LoginRequiredMixin, ListView):
    model = PortfolioItem
    template_name = "dashboard/portfolio_list.html"

    def get_queryset(self):
        return self.request.user.portfolio_items.all()


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("portfolio_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not form.cleaned_data.get("created_at"):
            form.instance.created_at = timezone.now().date()
        messages.success(self.request, "Проект добавлен.")
        return super().form_valid(form)


class PortfolioUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = "dashboard/form.html"
    success_url = reverse_lazy("portfolio_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_portfolio_form"] = True
        return context


class PortfolioDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = PortfolioItem
    template_name = "dashboard/portfolio_confirm_delete.html"
    success_url = reverse_lazy("portfolio_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Проект удалён.")
        return super().delete(request, *args, **kwargs)


class TestimonialListView(LoginRequiredMixin, ListView):
    model = Testimonial
    template_name = "dashboard/testimonial_list.html"

    def get_queryset(self):
        return self.request.user.testimonials.all()


class PublicTestimonialCreateView(LoginRequiredMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = "public/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.card_user = get_object_or_404(User, username=kwargs.get("username"))
        # запрет оставить отзыв самому себе
        if request.user == self.card_user:
            messages.error(request, "Нельзя оставить отзыв самому себе.")
            return redirect("card_detail", username=self.card_user.username)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.card_user
        form.instance.author = self.request.user
        form.instance.author_name = self.request.user.get_full_name() or self.request.user.username
        form.instance.author_title = self.request.user.title
        if not form.instance.created_at:
            form.instance.created_at = timezone.now().date()
        form.instance.is_published = True
        messages.success(self.request, "Отзыв добавлен.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("card_detail", kwargs={"username": self.card_user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_user"] = self.card_user
        return context



