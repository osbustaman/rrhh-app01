import datetime

from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError
from decouple import config

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from applications.security.api.serializer import CustomTokenObtainPairSerializer, CustomUserSerializer, UserSerializer
from applications.security.decorators import verify_token


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.none()  # Utiliza un queryset vacío porque no necesitamos ninguno
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Obtener el nombre de la base de datos de la solicitud
        db_name = request.data.get('database_name')
        
        # Validar que se proporcione el nombre de la base de datos
        if not db_name:
            return Response({"error": "Se requiere el nombre de la base de datos"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Cambiar la base de datos para el modelo de usuario
        User.objects.using(db_name)
        
        # Llama al método create del serializer para crear un nuevo usuario
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



