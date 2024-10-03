
from django.urls import path

from applications.employee.api.api import (
    CreateEmployeeView
    , EmployeeByUserIdView
    , GetDataUser
    , ListEmployees
    , RetrieveUserEmployee
    , RetrieveUserUserCompanyByUserId
    , UpdateUpdateMethodOfPaymentEmployee
    , UpdateUserCompanyByUserId
    , UpdateUserEmplEmployeeByUserId
    , UpdateUserEmployee,
    UploadFileView
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
    path('upload-file/', UploadFileView.as_view(), name='upload-file'),

    path('update-user-company/by-user/<int:user_id>/', UpdateUserCompanyByUserId.as_view(), name='update-user-company-by-user-id'),
    path('get-user-company/by-user/<int:user_id>/', RetrieveUserUserCompanyByUserId.as_view(), name='get-user-company'),
]