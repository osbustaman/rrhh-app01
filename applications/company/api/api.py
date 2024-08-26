from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from applications.company.api.serializer import BoxesCompensationSerializer, CompanySerializer, MutualSecuritySerializer, PostCompanySerializer
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
class PostCompany(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = PostCompanySerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = PostCompanySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Empresa creada correctamente'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Error al crear la empresa'}, status=status.HTTP_400_BAD_REQUEST)

@verify_token_cls
class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

@verify_token_cls
class CompanyRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@verify_token_cls
class ListSocialReazon(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    
    def get(self, request, *args, **kwargs):

        try:

            queryset = Company()
            bussines_social_reason =  queryset.BUSSINESS_SOCIAL_REASON

            response = []
            for i in bussines_social_reason:

                response.append({
                    'id': i[0],
                    'name': i[1]
                })

            return Response(response, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'message': 'Error al obtener las razones sociales'}, status=status.HTTP_400_BAD_REQUEST)