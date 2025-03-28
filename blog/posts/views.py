from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Post, Status
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = "posts/list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(is_archived=False, status__name="published").order_by('-created_on')

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            return qs.filter(status__name="published")
        return qs.filter(
            Q(status__name="published") |
            Q(status__name="draft", author=self.request.user)
        )

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/new.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.author = self.request.user

        if 'publish' in self.request.POST:
            status, _ = Status.objects.get_or_create(name="published")
        else:
            status, _ = Status.objects.get_or_create(name="draft")
        form.instance.status = status
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/edit.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        if 'publish' in self.request.POST:
            status, _ = Status.objects.get_or_create(name="published")
            messages.success(self.request, "Post published successfully!")
        else:
            status, _ = Status.objects.get_or_create(name="draft")
            messages.success(self.request, "Draft saved successfully!")

        form.instance.status = status
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/delete.html"
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)

class DraftsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/drafts.html"
    context_object_name = "drafts"

    def get_queryset(self):
        draft_status, created = Status.objects.get_or_create(name="draft")
        return Post.objects.filter(
            author=self.request.user,
            is_archived=False,
            status=draft_status
        ).order_by('-created_on')

class ArchivesListView(ListView):
    model = Post
    template_name = "posts/archives.html"
    context_object_name = "archived_posts"

    def get_queryset(self):
        return Post.objects.filter(is_archived=True).order_by('-created_on')

class ArchivePostView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post.author

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.is_archived = True
        post.save()
        messages.success(request, f"Post '{post.title}' has been archived.")
        return redirect('list')

class UnarchivePostView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post.author

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post.is_archived = False
        post.save()
        messages.success(request, f"Post '{post.title}' has been restored.")
        return redirect('archives')
