from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from applications.employee.models import Employee, UserCompany


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

# User Company data serializer
class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = (
                    'company', 
                    # 'position', 
                    # 'subsidiary', 
                    # 'uc_is_boss', 
                    # 'uc_estate_employee', 
                    # 'uc_workertype', 
                    # 'uc_contracttype', 
                    # 'uc_hiring_date', 
                    # 'uc_daterenewalcontract', 
                    # 'uc_weeklyhours', 
                    # 'uc_agreedworkdays',
                    # 'uc_gratification',
                    # 'uc_typegratification',
                    # 'uc_semanacorrida',
                    # 'uc_workersector',
                    'uc_type_user',
                )


# user remuneration data serializer
class UserRemunerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = (
                    'uc_familyassignment', 
                    'uc_family_allowance_section', 
                    'uc_familialloads', 
                    'uc_amountfamilyassignment', 
                    'uc_basesalary',
                    'uc_gratification',
                    'uc_typegratification',
                    'uc_semanacorrida',
                    'uc_workersector',
        )


# User Company Forecast data serializer
class UserCompanyForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = (
                    'afp', 
                    'health', 
                    'uc_ufisapre', 
                    'uc_funisapre'
                )
        

# Terminated user data serializer terminated user
class TerminatedUserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = (
                    'uc_datenotificationletternotice', 
                    'eu_enddate', 
                    'uc_causal', 
                    'uc_foundation',
                    'uc_tiponotication'
                )


# Employee serializer bank
class UpdateMethodOfPaymentEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'emp_id', 
            'emp_paymentformat', 
            'emp_accounttype', 
            'emp_bankaccount', 
            'bank'
        )


# Employee serializer
class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('emp_id',
                    'emp_foreign',
                    'emp_nationality',
                    'emp_rut',
                    'emp_sex',
                    'emp_birthdate',
                    'emp_civilstatus',
                    'emp_address',
                    'emp_studies',
                    'emp_studiesstatus',
                    'emp_title',
                    'emp_drivellicense',
                    'emp_typelicense',
                    'country',
                    'region',
                    'commune',
                    'emp_id', 'emp_paymentformat', 'emp_accounttype', 'emp_bankaccount', 'bank')

# User serializer
class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')


class CreateUserSerializer(serializers.ModelSerializer):
    rut = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'rut', 'email', 'first_name', 'last_name')


class EmployeeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', allow_null=True)
    full_name = serializers.SerializerMethodField()
    position_user = serializers.CharField(source='user.usercompany.position.pos_name_position', allow_null=True)
    rut = serializers.CharField(source='emp_rut')
    id_employee = serializers.IntegerField(source='emp_id')

    class Meta:
        model = Employee
        fields = ['user_id', 'id_employee', 'full_name', 'position_user', 'rut']

    def get_full_name(self, obj):
        # Manejar nombre completo
        if obj.user:
            return f"{obj.user.first_name.title()} {obj.user.last_name.title()}"
        return None
    
class UploadFileSerializer(serializers.Serializer):
    file_base64 = serializers.CharField()
    user_id = serializers.IntegerField()