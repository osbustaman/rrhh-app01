from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from applications.security.models import Country, Region, Commune, Customers
from remunerations.utils import validarRut


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        try:
            validate_email(data['email'])
        except ValidationError:
            raise serializers.ValidationError("El correo electrónico no es válido")

        return data

    def create(self, validated_data):
        # Hashea la contraseña antes de crear el usuario
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    
class CustomerSerializer(serializers.ModelSerializer):

    cus_representative_rut = serializers.CharField(max_length=10)
    cus_identifier = serializers.CharField(max_length=10)

    def validate_cus_identifier(self, value):
        if not validarRut(value):
            raise serializers.ValidationError("RUT del cliente no es válido")
        return value
    
    def validate_cus_representative_rut(self, value):
        if not validarRut(value):
            raise serializers.ValidationError("RUT del representante no es válido")
        return value

    class Meta:
        model = Customers
        fields = [
            'cus_name',
            'cus_identifier',
            'cus_email',
            'cus_representative_name',
            'cus_representative_rut',
            'cus_representative_mail',
            'cus_name_bd',
            'cus_date_in',
            'cus_date_out',
            'cus_number_users',
            'country_id',
            'region_id',
            'commune_id',
        ]