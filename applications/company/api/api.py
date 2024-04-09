from rest_framework import generics

from applications.company.api.serializer import BoxesCompensationSerializer, MutualSecuritySerializer
from applications.company.models import BoxesCompensation, MutualSecurity


class BoxesCompensationListCreate(generics.ListCreateAPIView):
    queryset = BoxesCompensation.objects.all()
    serializer_class = BoxesCompensationSerializer

class BoxesCompensationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoxesCompensation.objects.all()
    serializer_class = BoxesCompensationSerializer

class MutualSecurityListCreate(generics.ListCreateAPIView):
    queryset = MutualSecurity.objects.all()
    serializer_class = MutualSecuritySerializer

class MutualSecurityRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MutualSecurity.objects.all()
    serializer_class = MutualSecuritySerializer