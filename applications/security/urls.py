from django.urls import include, path

from applications.security.api.api_login import GetDataUserAdmin
from . import views

from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'security'

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourcompany.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[],
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('data-user', GetDataUserAdmin.as_view(), name='GetDataUserAdmin')
]

