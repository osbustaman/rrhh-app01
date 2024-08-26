
from django.urls import path

from applications.employee.api.api import GetDataUser


from . import views

urlpatterns = [
    path('data-user-customer/<int:pk>', GetDataUser.as_view(), name='data_user'),
]