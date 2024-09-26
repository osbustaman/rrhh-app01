from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from applications.employee.models import Employee


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

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