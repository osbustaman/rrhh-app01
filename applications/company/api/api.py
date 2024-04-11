from rest_framework import generics

from applications.company.api.serializer import BoxesCompensationSerializer, CompanySerializer, MutualSecuritySerializer
from applications.company.models import BoxesCompensation, Company, MutualSecurity
from remunerations.decorators import verify_token_cls

@verify_token_cls
class BoxesCompensationListCreate(generics.ListCreateAPIView):
    queryset = BoxesCompensation.objects.all()
    serializer_class = BoxesCompensationSerializer

#region BoxesCompensationListCreate
@verify_token_cls
class BoxesCompensationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoxesCompensation.objects.all()
    serializer_class = BoxesCompensationSerializer

@verify_token_cls
class MutualSecurityListCreate(generics.ListCreateAPIView):
    queryset = MutualSecurity.objects.all()
    serializer_class = MutualSecuritySerializer

@verify_token_cls
class MutualSecurityRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MutualSecurity.objects.all()
    serializer_class = MutualSecuritySerializer

@verify_token_cls
class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

@verify_token_cls
class CompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer