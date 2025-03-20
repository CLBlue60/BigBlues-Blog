from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Post
from django.urls import reverse_lazy

# Create your views here.
class PostUpdateView(UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "content", "author"]
    success_url = reverse_lazy('list')

class PostDeleteView(DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post
    context_object_name = "object_list"

class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post

class PostCreateView(CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "content", "author"]
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        print("Form is valid. Saving post...")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid. Errors:", form.errors)
        return super().form_invalid(form)

class AboutPageView(TemplateView):
    template_name = "pages/about.html"
