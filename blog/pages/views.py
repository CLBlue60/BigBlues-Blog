from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/home.html"

class AboutPageView(TemplateView):
    template_name = "pages/about.html"

class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

class SignupPageView(TemplateView):
    template_name = "registration/signup.html"

def home(request):
    return render(request, 'pages/home.html')
