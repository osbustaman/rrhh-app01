from django.urls import path

from applications.administrator.api.api import CreateUserView, ListAdminUsersView
from applications.administrator.views import add_admin

app_name = 'administrator_app'

urlpatterns = [

    path('add/user/admin/', add_admin, name='add_admin'),


    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('list-admin-users/', ListAdminUsersView.as_view(), name='list_admin_users'),
]
