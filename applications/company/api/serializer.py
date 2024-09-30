import re
from rest_framework import serializers

from applications.company.models import (
    Area,
    Bank
    , BoxesCompensation
    , CenterCost
    , Company
    , Department
    , MutualSecurity,
    Position
    , Subsidiary
)
from applications.company.models import Commune, Region

def validate_rut(rut):
    rut = (rut.replace(".", "").replace("-", "")).upper()  # Eliminar puntos y guiones
    if not re.match(r'^\d{1,8}[0-9K]$', rut):  # Verificar formato
        return False
    rut_sin_dv = rut[:-1]
    dv = rut[-1].upper()  # Obtener dígito verificador
    multiplicador = 2
    suma = 0
    for r in reversed(rut_sin_dv):
        suma += int(r) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2
    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    return dv == dv_calculado


def validate_mail(correo):
    # Patrón de expresión regular para validar un correo electrónico
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Se compila el patrón
    patron_compilado = re.compile(patron)

    # Se verifica si el correo coincide con el patrón
    if patron_compilado.match(correo):
        return True
    else:
        return False
    
    
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['ban_id', 'ban_name', 'ban_code', 'ban_active']


class PositionSerializer(serializers.ModelSerializer):
    dep_name = serializers.CharField(source='departament.dep_name', read_only=True)
    class Meta:
        model = Position
        fields = ['pos_id', 'pos_name_position', 'departament', 'dep_name', 'post_description', 'pos_active']


class DepartamentSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(source='area.ar_name', read_only=True)
    class Meta:
        model = Department
        fields = ['dep_id', 'dep_name', 'area', 'area_name', 'dep_description', 'dep_active']


class AreaSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.com_name_company', read_only=True)

    class Meta:
        model = Area
        fields = ['ar_id', 'ar_name', 'company', 'company_name', 'ar_active']


class CompanySerializer(serializers.ModelSerializer):
    def validate_com_rut(self, value):
        if not validate_rut(value):
            raise serializers.ValidationError("El Rut ingresado no es válido")
        return value

    def validate_com_rut_representative(self, value):
        if not validate_rut(value):
            raise serializers.ValidationError("El Rut del representante ingresado no es válido")
        return value

    def validate_com_rut_counter(self, value):
        if not validate_rut(value):
            raise serializers.ValidationError("El Rut del contador ingresado no es válido")
        return value

    def validate_com_mail_one(self, value):
        if not validate_mail(value):
            raise serializers.ValidationError("El correo electrónico 1 ingresado no es válido")
        return value

    def validate_com_mail_two(self, value):
        if value and not validate_mail(value):
            raise serializers.ValidationError("El correo electrónico 2 ingresado no es válido")
        return value


    class Meta:
        model = Company
        fields = '__all__'


class PostCompanySerializer(serializers.ModelSerializer):

    com_id_parent_company = serializers.CharField(max_length=1, required=False, default=None)


    def validate_com_rut(self, value):
        if not validate_rut(value):
            raise serializers.ValidationError("El Rut ingresado no es válido")
        return value

    def validate_com_rut_representative(self, value):
        if not validate_rut(value):
            raise serializers.ValidationError("El Rut del representante ingresado no es válido")
        return value


    def validate_com_mail_one(self, value):
        if not validate_mail(value):
            raise serializers.ValidationError("El correo electrónico 1 ingresado no es válido")
        return value

    def validate_com_mail_two(self, value):
        if value and not validate_mail(value):
            raise serializers.ValidationError("El correo electrónico 2 ingresado no es válido")
        return value
    
    def to_internal_value(self, data):
        # Lista de campos que necesitan ser convertidos de string a int
        fields_to_convert = ['commune', 'region', 'country']
        
        for field in fields_to_convert:
            if field in data:
                try:
                    data[field] = int(data[field])
                except ValueError:
                    raise serializers.ValidationError({field: f"Debe ser un número entero válido."})
        
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        # Asegurarse de que com_id_parent_company sea siempre null
        validated_data['com_id_parent_company'] = None
        return super().create(validated_data)

    class Meta:
        model = Company
        fields = [
            'com_rut'
            , 'com_name_company'
            , 'com_is_holding'
            , 'com_id_parent_company'
            , 'com_representative_name'
            , 'com_rut_representative'
            , 'com_is_state'
            , 'com_social_reason'
            , 'com_twist_company'
            , 'com_address'
            , 'commune'
            , 'region'
            , 'country'
            , 'com_phone_one'
            , 'com_phone_two'
            , 'com_mail_one'
            , 'com_mail_two'
        ]


class BoxesCompensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxesCompensation
        fields = '__all__'


class MutualSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualSecurity
        fields = '__all__'


class SubsidiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsidiary
        fields = [
            'sub_name'
            , 'sub_mail'
            , 'sub_phone'
            , 'sub_address'
            , 'commune'
            , 'region'
            , 'country'
            , 'sub_matrixhouse'
        ]


class GetSubsidiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsidiary
        fields = [
            'sub_id',
            'sub_name',
            'sub_mail',
            'sub_phone',
            'sub_address',
            'commune',
            'region',
            'sub_matrixhouse'
        ]


class CenterCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterCost
        fields = [
            'company',
            'cencost_name'
        ]


class ListCenterCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterCost
        fields = '__all__'


class ListCenterCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterCost
        fields = '__all__'