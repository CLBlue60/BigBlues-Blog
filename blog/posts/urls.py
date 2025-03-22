from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    DraftsListView,
    ArchivesListView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("new/", PostCreateView.as_view(), name="new"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
    path("drafts/", DraftsListView.as_view(), name="drafts"),
    path("archives/", ArchivesListView.as_view(), name="archives"),
]
