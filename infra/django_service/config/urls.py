from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse


def healthz(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz),
    # path("api/v1/", include("apps.users.urls")),
    # path("api/v1/", include("apps.analytics.urls")),
]
