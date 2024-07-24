from django.urls import path

from applications.administrator.api.api import (
    CreateUserView
    , ListAdminUsersView
    , ListCommuneView
    , ListCountriesView
    , ListRegionView
    , ListCustomersView
    , CreateCustomerView
    , GetCustomerDataView
    , UpdateCustomerView
)
from applications.administrator.views import add_admin

app_name = 'administrator_app'

urlpatterns = [

    path('add/user/admin/', add_admin, name='add_admin'),

    path('create-user/<int:pk>/', CreateUserView.as_view(), name='create_user'),
    path('list-admin-users/', ListAdminUsersView.as_view(), name='list_admin_users'),

    path('list-countries', ListCountriesView.as_view(), name='ListCountriesView'),
    path('list-region', ListRegionView.as_view(), name='ListRegionView'),
    path('list-commune', ListCommuneView.as_view(), name='ListCommuneView'),

    path('listado-clientes', ListCustomersView.as_view(), name='ListCustomersView'),
    path('add-customers', CreateCustomerView.as_view(), name='CreateCustomerView'),
    path('get-data-customer', CreateCustomerView.as_view(), name='CreateCustomerView'),

    path('get-data-customer/<int:pk>/', GetCustomerDataView.as_view(), name='CreateCustomerView'),
    path('update-data-customer/<int:pk>/', UpdateCustomerView.as_view(), name='UpdateCustomerView'),
]
