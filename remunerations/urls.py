"""remunerations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from applications.employee.api.api import LoginUser, LogoutUser
from applications.security.api.api_login import Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('login-drf', Login.as_view(), name='login-drf'),
    path('logout-drf', Logout.as_view(), name='logout-drf'),

    # Ruta para iniciar sesión, utiliza la clase Login que hemos definido
    path('login', LoginUser.as_view(), name='login'),

    # Ruta para cerrar sesión, utiliza la clase Logout que hemos definido
    path('logout', LogoutUser.as_view(), name='logout'),


    path('', include('applications.security.urls')),
    path('', include('applications.administrator.urls')),
    path('', include('applications.company.urls')),
    path('', include('applications.employee.urls')),


    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
