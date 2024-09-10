from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from applications.company.api.serializer import (
    AreaSerializer,
    BoxesCompensationSerializer
    , CenterCostSerializer
    , CompanySerializer,
    DepartamentSerializer
    , GetSubsidiarySerializer
    , ListCenterCostSerializer
    , MutualSecuritySerializer
    , PostCompanySerializer
    , SubsidiarySerializer
)
from applications.company.models import (
    Area,
    BoxesCompensation
    , CenterCost
    , Company
    , Department
    , MutualSecurity
    , Subsidiary
)
from remunerations.decorators import verify_token_cls


@verify_token_cls
class ListDepartament(generics.ListAPIView):
    serializer_class = DepartamentSerializer

    def get_queryset(self):
        # Filtrar solo las áreas activas (ar_active = 'Y')
        return Department.objects.filter(ar_active='Y')


@verify_token_cls
class ListArea(generics.ListAPIView):
    serializer_class = AreaSerializer

    def get_queryset(self):
        # Filtrar solo las áreas activas (ar_active = 'Y')
        return Area.objects.filter(ar_active='Y')


@verify_token_cls
class CreateArea(generics.CreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


@verify_token_cls
class RetrieveArea(generics.RetrieveAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    lookup_field = 'ar_id'


@verify_token_cls
class UpdateArea(generics.UpdateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    lookup_field = 'ar_id'


@verify_token_cls
class DeleteArea(generics.UpdateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    lookup_field = 'ar_id'

    def update(self, request, *args, **kwargs):
        # Buscar el área utilizando el 'ar_id'
        area = self.get_object()

        # Cambiar el estado del área a inactiva
        area.ar_active = 'N'
        area.save()

        return Response({'message': 'Área desactivada correctamente'}, status=status.HTTP_200_OK)


@verify_token_cls
class ListArea(generics.ListAPIView):
    serializer_class = AreaSerializer

    def get_queryset(self):
        # Filtrar solo las áreas activas (ar_active = 'Y')
        return Area.objects.filter(ar_active='Y')


@verify_token_cls
class ListAssociatedEntities(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    def get_queryset(self):
        return super().get_queryset().filter(company__com_id=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        try:
            company = self.get_object()
            serializer = CompanySerializer(company)

            objectMutualSecurity = MutualSecurity.objects.filter(ms_id=serializer.data['mutual_security']).first()
            objectBoxesCompensation = BoxesCompensation.objects.filter(bc_id=serializer.data['boxes_compensation']).first()

            data = {
                'mutual_security': objectMutualSecurity.ms_name,
                'boxes_compensation': objectBoxesCompensation.bc_fantasy_name,
                'mutual_security_id': objectMutualSecurity.ms_id,
                'boxes_compensation_id': objectBoxesCompensation.bc_id,
                'com_id': serializer.data['com_id']
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al obtener las sucursales: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class CreateAssociatedEntities(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        return super().get_queryset().filter(company__com_id=self.kwargs.get('pk')).first()


    def put(self, request, *args, **kwargs):
        try:
            data = request.data

            object_company = self.get_queryset()
            object_company.mutual_security = MutualSecurity.objects.filter(ms_id=int(data['mutual_security'])).first()
            object_company.boxes_compensation = BoxesCompensation.objects.filter(bc_id=int(data['boxes_compensation'])).first()
            object_company.save()

            return Response({'message': 'Entidades actualizadas con éxito'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al asociar las entidades'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class DeleteCenterCost(generics.RetrieveUpdateDestroyAPIView):
    queryset = CenterCost.objects.all()
    serializer_class = ListCenterCostSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, cencost_id=self.kwargs.get('pk'))
        return obj

    def put(self, request, *args, **kwargs):
        try:
            center_cost = self.get_object()
            center_cost.cencost_active = 'N'
            center_cost.save()
            return Response({'message': 'Centro de costo eliminado correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al eliminar el centro de costo'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class ListCenterCost(generics.ListCreateAPIView):
    queryset = CenterCost.objects.all()
    serializer_class = ListCenterCostSerializer

    def get_queryset(self):
        return super().get_queryset().filter(company__com_id=self.kwargs.get('pk'), cencost_active='Y')

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = ListCenterCostSerializer(queryset, many=True)
            data = serializer.data

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al obtener las sucursales: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class EditCenterCost(generics.RetrieveUpdateDestroyAPIView):
    queryset = CenterCost.objects.all()
    serializer_class = CenterCostSerializer

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = CenterCostSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                center_cost = serializer.save()
                response = {
                    'cencost_id': center_cost.cencost_id,
                    'message': 'Centro de costo actualizado con éxito'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Error al actualizar el centro de costo: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class GetCreateCenterCost(generics.RetrieveAPIView):
    queryset = CenterCost.objects.all()
    serializer_class = CenterCostSerializer

    def get(self, request, *args, **kwargs):
        try:
            center_cost = self.get_object()
            serializer = CenterCostSerializer(center_cost)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al obtener los datos del centro de costo'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class CreateCenterCost(generics.CreateAPIView):
    queryset = CenterCost.objects.all()
    serializer_class = CenterCostSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = CenterCostSerializer(data=request.data)
            if serializer.is_valid():
                center_cost = serializer.save()
                response = {
                    'cencost_id': center_cost.cencost_id,
                    'message': 'Centro de costo creado correctamente'
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Error al crear el centro de costo'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class DeleteSubsidiary(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subsidiary.objects.all()
    serializer_class = SubsidiarySerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, sub_id=self.kwargs.get('pk'))
        return obj

    def put(self, request, *args, **kwargs):
        try:
            subsidiary = self.get_object()
            subsidiary.sub_active = 'N'
            subsidiary.save()
            return Response({'message': 'Sucursal eliminada correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al eliminar la sucursal'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class EditSubsidiary(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subsidiary.objects.all()
    serializer_class = SubsidiarySerializer

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SubsidiarySerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                subsidiary = serializer.save()
                response = {
                    'com_id': subsidiary.sub_id,
                    'message': 'Sucursal actualizada con éxito'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f'Error al actualizar la empresa: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class ListSubsidiary(generics.ListCreateAPIView):
    queryset = Subsidiary.objects.all()
    serializer_class = GetSubsidiarySerializer

    def get_queryset(self):
        return super().get_queryset().filter(company__com_id=self.kwargs.get('pk'), sub_active='Y')

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = GetSubsidiarySerializer(queryset, many=True)
            data = serializer.data

            for index, i in enumerate(queryset):
                data[index]['commune_name'] = i.commune.com_name
                data[index]['region_name'] = i.region.re_name

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al obtener las sucursales: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class GetSubsidiary(generics.RetrieveAPIView):
    queryset = Subsidiary.objects.all()
    serializer_class = SubsidiarySerializer

    def get(self, request, *args, **kwargs):
        try:
            subsidiary = self.get_object()
            serializer = SubsidiarySerializer(subsidiary)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al obtener la sucursal'}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class CreateSubsidiary(generics.CreateAPIView):
    queryset = Subsidiary.objects.all()
    serializer_class = SubsidiarySerializer

    def post(self, request, *args, **kwargs):
        try:
            com_id = kwargs.get('pk')

            # Obtener los datos de la solicitud
            serializer = SubsidiarySerializer(data=request.data)
            if serializer.is_valid():
                sub_name = serializer.validated_data.get('sub_name')
                sub_address = serializer.validated_data.get('sub_address')

                # Comprobar si ya existe una sucursal con el mismo nombre y dirección
                if Subsidiary.objects.filter(sub_name=sub_name, sub_address=sub_address).exists():
                    return Response({'message': 'La sucursal ya existe.'}, status=status.HTTP_400_BAD_REQUEST)

                # Obtener la compañía
                obj_company = Company.objects.filter(com_id=com_id).first()
                if not obj_company:
                    return Response({'message': 'La compañía no existe.'}, status=status.HTTP_400_BAD_REQUEST)

                # Crear la nueva sucursal con la compañía
                subsidiary = serializer.save(company=obj_company)

                response = {
                    'sub_id': subsidiary.sub_id,
                    'message': 'Sucursal creada correctamente'
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': f"Error al crear la sucursal: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class BoxesCompensationListCreate(generics.ListCreateAPIView):
    queryset = BoxesCompensation.objects.all()
    serializer_class = BoxesCompensationSerializer


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
class DeleteCompany(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = PostCompanySerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, com_id=self.kwargs.get('pk'))
        return obj

    def put(self, request, *args, **kwargs):
        try:
            company = self.get_object()
            company.com_active = 'N'
            company.save()
            return Response({'message': 'Empresa eliminada correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al eliminar la empresa'}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'message': f"Error al crear la empresa {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@verify_token_cls
class CompanyListCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = Company.objects.filter(com_active='Y')
            serializer = CompanySerializer(queryset, many=True)
            data = serializer.data

            for index, i in enumerate(queryset):
                data[index]['commune_name'] = i.commune.com_name
                data[index]['region_name'] = i.region.re_name

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Error al obtener las empresas: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


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