from django.urls import path

from applications.company.api.api import (
    BoxesCompensationListCreate, 
    BoxesCompensationRetrieveUpdateDestroy,
    CreateArea,
    CreateAssociatedEntities,
    CreateCenterCost,
    CreateDepartment,
    CreatePosition,
    CreateSubsidiary,
    DeleteArea,
    DeleteCenterCost,
    DeleteCompany,
    DeleteDepartment,
    DeletePosition,
    DeleteSubsidiary,
    EditCenterCost,
    EditCompany,
    EditSubsidiary,
    GetCompany,
    GetCreateCenterCost,
    GetSubsidiary,
    ListArea,
    ListAssociatedEntities,
    ListBanksView,
    ListCenterCost,
    ListDepartament,
    ListPosition,
    ListSocialReazon,
    ListSubsidiary, 
    MutualSecurityListCreate, 
    MutualSecurityRetrieveUpdateDestroy,
    CompanyListCreate,
    ListSocialReazon,
    PostCompany,
    RetrieveArea,
    RetrieveDepartment,
    RetrievePosition,
    UpdateArea,
    UpdateDepartment,
    UpdatePosition
)

urlpatterns = [
    path('boxes-compensation/', BoxesCompensationListCreate.as_view(), name='boxes_compensation_list_create'),
    path('boxes-compensation/<int:pk>/', BoxesCompensationRetrieveUpdateDestroy.as_view(), name='boxes_compensation_detail'),
    path('mutual-security/', MutualSecurityListCreate.as_view(), name='mutualsecurity-list-create'),
    path('mutual-security/<int:pk>/', MutualSecurityRetrieveUpdateDestroy.as_view(), name='mutualsecurity-retrieve-update-destroy'),
    path('list-companies', CompanyListCreate.as_view(), name='list-companies'),
    path('create-company', PostCompany.as_view(), name='create-company'),
    path('edit-company/<int:pk>/', EditCompany.as_view(), name='edit-company'),
    path('view-company/<int:pk>/', GetCompany.as_view(), name='view-company'),
    path('delete-company/<int:pk>/', DeleteCompany.as_view(), name='delete-company'),

    path('list-banks', ListBanksView.as_view(), name='ListBanksView'),
    
    path('create-branch-office/<int:pk>/', CreateSubsidiary.as_view(), name='create-branch-office'),
    path('view-branch-office/<int:pk>/', GetSubsidiary.as_view(), name='create-branch-office'),
    path('list-branch-office/<int:pk>/', ListSubsidiary.as_view(), name='list-branch-office'),
    path('edit-branch-office/<int:pk>/', EditSubsidiary.as_view(), name='edit-branch-office'),
    path('delete-branch-office/<int:pk>/', DeleteSubsidiary.as_view(), name='delete-branch-office'),

    path('create-center-cost/<int:pk>/', CreateCenterCost.as_view(), name='create-center-cost'),
    path('view-center-cost/<int:pk>/', GetCreateCenterCost.as_view(), name='view-create-center-cost'),
    path('edit-center-cost/<int:pk>/', EditCenterCost.as_view(), name='edit-center-cost'),
    path('list-center-cost/<int:pk>/', ListCenterCost.as_view(), name='list-center-cost'),
    path('delete-center-cost/<int:pk>/', DeleteCenterCost.as_view(), name='delete-center-cost'),

    path('create-associated-entities/<int:pk>/', CreateAssociatedEntities.as_view(), name='create-associated-entities'),
    path('get-associated-entities/<int:pk>/', ListAssociatedEntities.as_view(), name='get-associated-entities'),

    path('list-reason-social', ListSocialReazon.as_view(), name='list-reason-social'),

    # area ********************************************************************************************
    path('add-areas/create/', CreateArea.as_view(), name='create-area'),
    path('get-areas/<int:ar_id>/', RetrieveArea.as_view(), name='retrieve-area'),
    path('update-areas/<int:ar_id>/', UpdateArea.as_view(), name='update-area'),
    path('delete-area/<int:ar_id>/', DeleteArea.as_view(), name='delete-area'),
    path('list-areas/', ListArea.as_view(), name='list-areas'),
    # area ********************************************************************************************

    # departament *************************************************************************************
    path('list-departament/<int:ar_id>/', ListDepartament.as_view(), name='list-departament'),
    path('add-department/create/', CreateDepartment.as_view(), name='create-department'),
    path('delete-department/<int:dep_id>/', DeleteDepartment.as_view(), name='delete-department'),
    path('update-department/<int:dep_id>/', UpdateDepartment.as_view(), name='update-department'),
    path('get-department/<int:dep_id>/', RetrieveDepartment.as_view(), name='retrieve-department'),
    # departament *************************************************************************************
    
    # position ****************************************************************************************
    path('list-position/<int:dep_id>/', ListPosition.as_view(), name='list-position'),
    path('add-position/create/', CreatePosition.as_view(), name='create-position'),
    path('delete-position/<int:pos_id>/', DeletePosition.as_view(), name='delete-position'),
    path('update-position/<int:pos_id>/', UpdatePosition.as_view(), name='update-position'),
    path('get-position/<int:pos_id>/', RetrievePosition.as_view(), name='retrieve-position'),
    # position ****************************************************************************************

]