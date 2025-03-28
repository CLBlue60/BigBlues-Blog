from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  
    path("accounts/", include("blog.users.urls")),
    path("", include("blog.pages.urls")),
]
