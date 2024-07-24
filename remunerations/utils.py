import datetime
import re

from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.core.exceptions import ObjectDoesNotExist

from decouple import config


# Lista negra para almacenar tokens revocados
blacklist = set()

def expire_date(days: int):
    now = datetime.datetime.now()
    new_date = now + datetime.timedelta(days)
    return new_date

def write_token(data: dict):
    refresh = RefreshToken()
    token = encode(payload={**data, 'exp': expire_date(int(config('EXPIRE_DATE'))), 'jti': str(refresh.access_token)}, key=config('SECRET_KEY'), algorithm='HS256')
    return token.encode('UTF-8')

def decode_token(token: str):
    try:
        # Verificar si el token está en la lista negra
        if token in blacklist:
            return None

        decoded_token = decode(token, key=config('SECRET_KEY'), algorithms=['HS256'])
        return decoded_token
    except ExpiredSignatureError:
        # Manejar error de token expirado
        return None
    except InvalidSignatureError:
        # Manejar error de token inválido
        return None

def revoke_token(token: str):
    try:
        # Crear un objeto RefreshToken
        refresh_token = RefreshToken(token)
        
        # Verificar que el token es de tipo refresh
        if refresh_token.token_type != 'refresh':
            raise ValueError('El token no es de tipo refresh')

        # Obtener o crear el OutstandingToken
        outstanding_token, created = OutstandingToken.objects.get_or_create(
            jti=refresh_token['jti'],
            defaults={
                'token': str(refresh_token),
                'user': refresh_token['user'],
                'created_at': datetime.datetime.now(),
                'expires_at': refresh_token['exp']
            }
        )

        # Añadir el OutstandingToken a la lista negra
        BlacklistedToken.objects.create(token=outstanding_token)
        return {
            'message': 'Token revocado con éxito',
            'success': True
        }
    except Exception as e:
        return {
            'message': f'Error revoking token: {e}',
            'success': False
        }
    
def validarRut(rut):
    rut = rut.replace(".", "").replace("-", "")  # Eliminar puntos y guiones
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