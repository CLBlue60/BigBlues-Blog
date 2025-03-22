from django.urls import path
from .views import HomePageView, AboutPageView, ContactPageView, SignupPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),  # Home page
    path("about/", AboutPageView.as_view(), name="about"),  # About page
    path("contact/", ContactPageView.as_view(), name="contact"),  # Contact page
    path("signup/", SignupPageView.as_view(), name="signup"),  # Signup page
]
