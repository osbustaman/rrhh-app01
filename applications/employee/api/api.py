from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.db.models import F, Value, CharField, Q
from django.db.models.functions import Concat

from applications.employee.api.serializer import EmployeeSerializer, LoginTokenObtainPairSerializer, LoginUserSerializer
from applications.employee.models import Employee
from remunerations.decorators import verify_token_cls
from remunerations.utils import decode_token


@verify_token_cls
class ListEmployees(generics.ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)

        if pk:
            return Employee.objects.filter(
                user__usercompany__company_id=pk
            ).annotate(
                full_name=Concat('user__first_name', Value(' '), 'user__last_name'),
                id_employee=F('emp_id'),
                rut=F('emp_rut'),
                position_user=F('user__usercompany__position__pos_name_position')
            ).order_by('full_name', 'rut')

        return Employee.objects.all().annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name'),
            id_employee=F('emp_id'),
            rut=F('emp_rut'),
            position_user=F('user__usercompany__position__pos_name_position')
        ).order_by('full_name', 'rut')

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IndexError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


@verify_token_cls
class GetDataUser(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['pk']
        
        user = User.objects.filter(id=user_id).first()
        if user:
            user_serializer = LoginUserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'No existe este usuario'}, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(TokenObtainPairView):
    serializer_class = LoginTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)

        if user:
            # Verificar si ya existe un token activo para el usuario
            # active_token = cache.get(f'user_token_{user.id}')
            # if active_token:
            #     return Response({
            #         'error': 'Sesión activa detectada con las mismas credenciales.'
            #     }, status=status.HTTP_409_CONFLICT)

            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = LoginUserSerializer(user)
                access_token = login_serializer.validated_data.get('access')
                refresh_token = login_serializer.validated_data.get('refresh')

                # Guardar token en cache para detectar sesiones simultáneas
                cache.set(f'user_token_{user.id}', access_token, timeout=3600)

                return Response({
                    'token': access_token,
                    'user': user_serializer.data['id'],
                    'message': 'Inicio de sesión exitoso'
                }, status=status.HTTP_200_OK)

            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class LogoutUser(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.headers.get("token")
        get_decode_token = decode_token(token)
        user_id = get_decode_token.get('user_id')
        
        user = User.objects.filter(id=user_id).first()
        if user:
            # Invalidar el token
            RefreshToken.for_user(user)
            
            # Eliminar el token de la cache
            cache.delete(f'user_token_{user.id}')
            
            return Response({'message': 'Sesión cerrada con éxito'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'No existe este usuario'}, status=status.HTTP_400_BAD_REQUEST)
