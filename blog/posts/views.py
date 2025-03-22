from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)

from .models import Post, Status
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import get_object_or_404

STATUS_DRAFT = "Draft"
STATUS_PUBLISHED = "Published"
STATUS_ARCHIVED = "Archived"

# Create your views here.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "content"]
    success_url = reverse_lazy('list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Status.objects.get(name=STATUS_PUBLISHED)
        context["title"] = "Published"
        context["post_list"] = (
            Post.objects
            .filter(status=published)
            .order_by("created_on").reverse()
        )
        return context

class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post

    def get(self, request, *args, **kwargs):
        post = self.get_object()


        if post.status.name == STATUS_PUBLISHED:
            return super().get(request, *args, **kwargs)
        elif post.status.name == STATUS_DRAFT and post.author == request.user:
            return super().get(request, *args, **kwargs)
        elif post.status.name == STATUS_ARCHIVED and request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

from django.shortcuts import get_object_or_404

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "content"]
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        draft_status = get_object_or_404(Status, name="Draft")
        form.instance.status = draft_status
        return super().form_valid(form)

class DraftsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/drafts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drafts = Status.objects.get(name=STATUS_DRAFT)
        context["title"] = "Drafts"
        context["post_list"] = (
            Post.objects
            .filter(status=drafts)
            .filter(author=self.request.user)
            .order_by("created_on").reverse()
        )
        return context

class ArchivesListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/archives.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archived_status = get_object_or_404(Status, name=STATUS_ARCHIVED)
        context["post_list"] = (
            Post.objects
            .filter(status=archived_status)
            .order_by("-updated_at")
        )
        return context

class AboutPageView(TemplateView):
    template_name = "pages/about.html"


def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
