from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Status
from .forms import PostForm


# Post List View
class PostListView(ListView):
    model = Post
    template_name = "blog/posts/post_list.html"
    context_object_name = "posts"


# Post Detail View
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/posts/post_detail.html"
    context_object_name = "post"


# Post Create View
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/posts/post_form.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Post Update View
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/posts/post_form.html"
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Post Delete View
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/posts/post_confirm_delete.html"
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# About Page View
class AboutPageView(TemplateView):
    template_name = "blog/pages/about.html"


# Contact Page View
class ContactPageView(TemplateView):
    template_name = "blog/pages/contact.html"


# Signup Page View
class SignupPageView(TemplateView):
    template_name = "registration/signup.html"

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return HttpResponseRedirect(reverse_lazy("login"))
        return self.render_to_response({"form": form})

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return self.render_to_response({"form": form})
