from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    path("social-links/", views.SocialLinkListView.as_view(), name="social_links"),
    path("social-links/add/", views.SocialLinkCreateView.as_view(), name="social_link_add"),
    path("social-links/<int:pk>/", views.SocialLinkUpdateView.as_view(), name="social_link_edit"),
    path("portfolio/", views.PortfolioListView.as_view(), name="portfolio_list"),
    path("portfolio/add/", views.PortfolioCreateView.as_view(), name="portfolio_add"),
    path("portfolio/<int:pk>/", views.PortfolioUpdateView.as_view(), name="portfolio_edit"),
    path("portfolio/<int:pk>/delete/", views.PortfolioDeleteView.as_view(), name="portfolio_delete"),
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonial_list"),
]

