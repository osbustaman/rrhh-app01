from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from applications.employee.models import Employee


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


# Employee serializer bank
class UpdateMethodOfPaymentEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('emp_id', 'emp_paymentformat', 'emp_accounttype', 'emp_bankaccount', 'bank')


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
                    'commune')

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