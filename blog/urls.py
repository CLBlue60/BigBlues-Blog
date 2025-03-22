from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("blog.pages.urls")),
]

if DEBUG:
    urlpatterns += [
        path('403/', custom_403_view),
        path('404/', custom_404_view),
        path('500/', custom_500_view),
    ]
