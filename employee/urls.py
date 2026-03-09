from django.urls import path
from .views import EmployeeAPI

urlpatterns = [

    path('employees/', EmployeeAPI.as_view()),
    path('employees/<int:id>/', EmployeeAPI.as_view()),
]