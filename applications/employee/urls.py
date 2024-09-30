
from django.urls import path

from applications.employee.api.api import (
    CreateEmployeeView
    , EmployeeByUserIdView
    , GetDataUser
    , ListEmployees
    , RetrieveUserEmployee,
    UpdateUpdateMethodOfPaymentEmployee
    , UpdateUserEmplEmployeeByUserId
    , UpdateUserEmployee
)


from . import views

urlpatterns = [
    path('data-user-customer/<int:pk>', GetDataUser.as_view(), name='data_user'),
    
    path('list-employees/<int:pk>/', ListEmployees.as_view(), name='list-employees-with-pk'),
    path('list-employees/', ListEmployees.as_view(), name='list-employees-no-pk'),
    path('create-employee/', CreateEmployeeView.as_view(), name='create-employee'),
    path('get-employee/<int:id>/', RetrieveUserEmployee.as_view(), name='retrieve-employee'),
    path('update-employee/<int:id>/', UpdateUserEmployee.as_view(), name='update-employee'),
    path('employee/by-user/<int:user_id>/', EmployeeByUserIdView.as_view(), name='employee-by-user-id'),
    path('update-employee/by-user/<int:user_id>/', UpdateUserEmplEmployeeByUserId.as_view(), name='update-employee-by-user-id'),
    path('update-method-of-payment/by-user/<int:user_id>/', UpdateUpdateMethodOfPaymentEmployee.as_view(), name='update-method-of-payment-by-user-id'),
]