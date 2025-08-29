from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("wosoapi/", include("api.urls")),
    path("wosoapi/", include("accounts.urls")),
]
