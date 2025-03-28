from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignUpForm  

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        messages.success(self.request, "Registration successful!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
