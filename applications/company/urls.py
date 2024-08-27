from django.urls import path

from applications.company.api.api import (
    BoxesCompensationListCreate, 
    BoxesCompensationRetrieveUpdateDestroy,
    EditCompany,
    GetCompany,
    ListSocialReazon, 
    MutualSecurityListCreate, 
    MutualSecurityRetrieveUpdateDestroy,
    CompanyListCreate,
    ListSocialReazon,
    PostCompany
)
from . import views

urlpatterns = [
    path('boxes-compensation/', BoxesCompensationListCreate.as_view(), name='boxes_compensation_list_create'),
    path('boxes-compensation/<int:pk>/', BoxesCompensationRetrieveUpdateDestroy.as_view(), name='boxes_compensation_detail'),
    path('mutual-security/', MutualSecurityListCreate.as_view(), name='mutualsecurity-list-create'),
    path('mutual-security/<int:pk>/', MutualSecurityRetrieveUpdateDestroy.as_view(), name='mutualsecurity-retrieve-update-destroy'),
    path('list-companies', CompanyListCreate.as_view(), name='list-companies'),
    path('create-company', PostCompany.as_view(), name='create-company'),
    path('edit-company/<int:pk>/', EditCompany.as_view(), name='edit-company'),
    path('view-company/<int:pk>/', GetCompany.as_view(), name='view-company'),
    
    path('list-reason-social', ListSocialReazon.as_view(), name='list-reason-social'),
    
]