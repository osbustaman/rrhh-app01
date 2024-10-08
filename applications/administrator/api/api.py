from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from applications.administrator.api.serializer import CustomerSerializer, CommuneSerializer, RegionSerializer, UserSerializer, CountriesSerializer
from applications.security.models import Country, Region, Commune, Customers
from remunerations.decorators import verify_token, verify_token_cls


@verify_token_cls
class ListCountriesView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountriesSerializer

@verify_token_cls
class ListRegionView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

@verify_token_cls
class ListCommuneView(generics.ListAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer

@verify_token_cls
class CreateCustomerView(generics.CreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        customer_id = serializer.instance.cus_id
        return Response({'cus_id': customer_id}, status=status.HTTP_201_CREATED, headers=headers)
    

@verify_token_cls
class UpdateCustomerView(generics.UpdateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@verify_token_cls
class GetCustomerDataView(generics.RetrieveAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        # Obtener el listado de clientes
        try:
            queryset = Customers.objects.filter(cus_id=(self.kwargs['pk']), cus_active='Y').first()
        except Customers.DoesNotExist:
            queryset = None
        return queryset

    def get(self, request, *args, **kwargs):

        if not self.get_queryset():
            message = {
                'error': 'No se encontró el cliente',
                'success': False
            }

            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        customers_objects = self.get_queryset()
        serializer = self.get_serializer(customers_objects)
        return Response(serializer.data, status=status.HTTP_200_OK)

@verify_token_cls
class GetDataCustomerView(generics.RetrieveAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ListCustomersView(generics.ListAPIView):
    queryset = Customers.objects.all()
    # serializer_class = CustomerSerializer

    def get_queryset(self):
        # Obtener el listado de clientes
        queryset = Customers.objects.filter(cus_active='Y')
        return queryset

    @verify_token
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            list_customers = []
            for customer in queryset:
                list_customers.append({
                    'cus_id': customer.cus_id,
                    'cus_name': customer.cus_name,
                    'cus_identifier': customer.cus_identifier,
                    'cus_email': customer.cus_email,
                    'cus_representative_name': customer.cus_representative_name,
                    'cus_representative_rut': customer.cus_representative_rut,
                    'cus_representative_mail': customer.cus_representative_mail,
                    'cus_name_bd': customer.cus_name_bd,
                    'cus_date_in': customer.cus_date_in,
                    'cus_date_out': customer.cus_date_out,
                    'cus_number_users': customer.cus_number_users
                })

            return Response(list_customers, status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

@verify_token_cls
class ListAdminUsersView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self, pk):
        # Obtener el nombre de la base de datos de la solicitud
        instance_customers = Customers.objects.filter(cus_id=pk).first()
        db_name = instance_customers.cus_name_bd
        
        # Validar que se proporcione el nombre de la base de datos
        if not db_name:
            raise ValueError("Se requiere el nombre de la base de datos")
        
        # Cambiar la base de datos para el modelo de usuario
        queryset = User.objects.using(db_name).filter(is_staff=True, is_superuser=True)
        return queryset

    @verify_token
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset(kwargs['pk'])
            serializer = self.serializer_class(queryset, many=True)
            
            # Obtener el nombre de la base de datos de la solicitud
            instance_customers = Customers.objects.filter(cus_id=kwargs['pk']).first()
            db_name = instance_customers.cus_name_bd
            
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

@verify_token_cls
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.none()  # Utiliza un queryset vacío porque no necesitamos ninguno
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        instance_customers = Customers.objects.filter(cus_id=kwargs['pk']).first()
        db_name = instance_customers.cus_name_bd

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
    
    