from django.urls import path
from .views import HomePageView, AboutPageView, SignupPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("signup/", SignupPageView.as_view(), name="signup"), 
]
