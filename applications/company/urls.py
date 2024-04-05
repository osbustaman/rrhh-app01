from django.urls import path

from applications.company.api.api import BoxesCompensationListCreate, BoxesCompensationRetrieveUpdateDestroy
from . import views

urlpatterns = [
    path('boxes-compensation/', BoxesCompensationListCreate.as_view(), name='boxes_compensation_list_create'),
    path('boxes-compensation/<int:pk>/', BoxesCompensationRetrieveUpdateDestroy.as_view(), name='boxes_compensation_detail'),
]