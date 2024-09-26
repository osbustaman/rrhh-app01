
from django.urls import path

from applications.employee.api.api import GetDataUser, ListEmployees


from . import views

urlpatterns = [
    path('data-user-customer/<int:pk>', GetDataUser.as_view(), name='data_user'),


    path('list-employees/<int:pk>/', ListEmployees.as_view(), name='list-employees-with-pk'),
    path('list-employees/', ListEmployees.as_view(), name='list-employees-no-pk'),

]