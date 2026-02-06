from django.urls import path
from team.views import get_employees

urlpatterns = [
    path("get_employees", get_employees),
    path("get_employees/", get_employees),
]
