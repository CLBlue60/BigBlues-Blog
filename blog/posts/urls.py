from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    DraftsListView,
    ArchivesListView,
    ArchivePostView,
    UnarchivePostView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("new/", PostCreateView.as_view(), name="new"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
    path("<int:pk>/archive/", ArchivePostView.as_view(), name="archive"),
    path("<int:pk>/unarchive/", UnarchivePostView.as_view(), name="unarchive"),
    path("drafts/", DraftsListView.as_view(), name="drafts"),
    path("archives/", ArchivesListView.as_view(), name="archives"),
]
