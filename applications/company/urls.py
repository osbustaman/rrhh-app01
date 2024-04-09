from django.urls import path

from applications.company.api.api import (
    BoxesCompensationListCreate, 
    BoxesCompensationRetrieveUpdateDestroy, 
    MutualSecurityListCreate, 
    MutualSecurityRetrieveUpdateDestroy
)
from . import views

urlpatterns = [
    path('boxes-compensation/', BoxesCompensationListCreate.as_view(), name='boxes_compensation_list_create'),
    path('boxes-compensation/<int:pk>/', BoxesCompensationRetrieveUpdateDestroy.as_view(), name='boxes_compensation_detail'),
    path('mutual-security/', MutualSecurityListCreate.as_view(), name='mutualsecurity-list-create'),
    path('mutual-security/<int:pk>/', MutualSecurityRetrieveUpdateDestroy.as_view(), name='mutualsecurity-retrieve-update-destroy'),
]