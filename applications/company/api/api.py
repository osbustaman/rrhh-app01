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
class GetCompany(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get(self, request, *args, **kwargs):
        try:
            company = self.get_object()
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al obtener la empresa'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class EditCompany(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = CompanySerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                company = serializer.save()
                response = {
                    'com_id': company.com_id,
                    'message': 'Empresa creada correctamente'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Error al actualizar la empresa'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class PostCompany(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = PostCompanySerializer

    def post(self, request, *args, **kwargs):
        try:
            com_rut = request.data.get('com_rut')
            if Company.objects.filter(com_rut=com_rut).exists():
                return Response({'message': 'La empresa ya existe'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = PostCompanySerializer(data=request.data)
            if serializer.is_valid():
                company = serializer.save()
                
                if request.data['com_id_parent_company']:
                    Company.objects.filter(com_id=company.com_id).update(com_id_parent_company=company)

                response = {
                    'com_id': company.com_id,
                    'message': 'Empresa creada correctamente'
                }

                return Response(response, status=status.HTTP_201_CREATED)
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