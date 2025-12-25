from django.urls import path

from .views import (
    CardDetailView,
    CustomLoginView,
    HomeView,
    PublicTestimonialCreateView,
    SignupView,
    UserSearchView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("search/", UserSearchView.as_view(), name="user_search"),
    path("card/<slug:username>/", CardDetailView.as_view(), name="card_detail"),
    path(
        "card/<slug:username>/review/",
        PublicTestimonialCreateView.as_view(),
        name="card_review",
    ),
]

