from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from applications.administrator.api.serializer import CustomerSerializer, UserSerializer
from applications.security.models import Customers
from remunerations.decorators import verify_token

class ListAdminUsersView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        # Obtener el nombre de la base de datos de la solicitud
        db_name = self.request.query_params.get('database_name')
        
        # Validar que se proporcione el nombre de la base de datos
        if not db_name:
            raise ValueError("Se requiere el nombre de la base de datos")
        
        # Cambiar la base de datos para el modelo de usuario
        queryset = User.objects.using(db_name).filter(is_staff=True, is_superuser=True)
        return queryset

    @verify_token
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            
            # Obtener el nombre de la base de datos de la solicitud
            db_name = request.query_params.get('database_name')
            
            # Incluir el nombre de la base de datos en la respuesta
            data = {
                'database_name': db_name,
                'users': serializer.data
            }
            return Response(data)
        except ValueError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.none()  # Utiliza un queryset vacío porque no necesitamos ninguno
    serializer_class = UserSerializer

    @verify_token
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
            # self.perform_create(serializer)
            # headers = self.get_success_headers(serializer.data)
            user = User()
            user.username = request.data.get('username')
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')
            user.email = request.data.get('email')
            user.set_password(request.data.get('password'))
            user.is_staff = True
            user.is_superuser = True
            user.save(using=db_name)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListCustomersView(generics.ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        # Obtener el listado de clientes
        queryset = Customers.objects.filter(cus_active='Y')
        return queryset

    @verify_token
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            
            # Incluir el nombre de la base de datos en la respuesta
            data = {
                'customers': serializer.data
            }
            return Response(data)
        except ValueError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
