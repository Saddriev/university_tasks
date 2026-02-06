from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.views.decorators.http import require_GET


@require_GET
def home(request):
    """Главная: список доступных эндпоинтов."""
    return JsonResponse({
        "message": "FitnessKit 1C API",
        "endpoints": {
            "employees": "/team/get_employees",
            "admin": "/admin/",
        },
    }, json_dumps_params={"ensure_ascii": False})


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("team/", include("team.urls")),
]
