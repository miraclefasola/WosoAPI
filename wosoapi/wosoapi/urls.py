from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("Madmin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/", include("accounts.urls")),
    path("", include("core.urls")),
]
from django.conf import settings


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
