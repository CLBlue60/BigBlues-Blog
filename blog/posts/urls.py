from django.urls import path
from blog.posts import views

urlpatterns = [
    path("list/", views.PostListView.as_view(), name="list"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("new/", views.PostCreateView.as_view(), name="new"), 
]
