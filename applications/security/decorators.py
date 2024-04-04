from decouple import config
from functools import wraps
from jwt import DecodeError, encode, decode, ExpiredSignatureError, InvalidSignatureError
from rest_framework.response import Response
from rest_framework import status


def get_auth_token(request):
    """
    Retrieves the authentication token from the request headers.

    Args:
        request: The HTTP request object.

    Returns:
        The authentication token if found in the headers, otherwise None.
    """
    auth_header = request.headers.get('token')
    if auth_header is not None and ' ' in auth_header:
        parts = auth_header.split(' ')
        if len(parts) == 2:
            return parts[1]
    return None


def verify_token(func):
    """
    Decorator function to verify the token in the request headers.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        ExpiredSignatureError: If the token has expired.
        InvalidSignatureError: If the token signature is invalid.
        DecodeError: If there is an error decoding the token.

    """
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        secret = config('SECRET_KEY')

        encoded_token = request.headers.get("token", False)
        if encoded_token:
            if ((len(encoded_token) > 0) and (encoded_token.count('.') <= 3)):
                try:
                    decode(encoded_token, secret, algorithms=["HS256"])
                    return func(self, request, *args, **kwargs)
                except ExpiredSignatureError:
                    return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
                except InvalidSignatureError:
                    return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
                except DecodeError:
                    return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)   
            
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper
