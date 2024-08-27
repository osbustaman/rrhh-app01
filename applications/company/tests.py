from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applications.company.models import Company


class PostCompanyTest(APITestCase):

    def setUp(self):
        # Configuración inicial antes de cada prueba
        self.valid_data = {
            'com_rut': '12345678-9',
            'com_name_company': 'Empresa Test',
            'com_rut_representative': '23456789-0',
            'com_is_state': 'N',
            'com_social_reason': 1,
            'com_twist_company': 'Servicios',
            'com_address': 'Calle Falsa 123',
            'country': 1,  # Ajustar con un ID válido existente
            'region': 1,   # Ajustar con un ID válido existente
            'commune': 1,  # Ajustar con un ID válido existente
            'com_phone_one': '123456789',
            'com_mail_one': 'email@empresa.cl',
        }

    def test_create_company_success(self):
        """
        Prueba la creación exitosa de una empresa.
        """
        response = self.client.post(reverse('post_company'), data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('com_id', response.data)
        self.assertEqual(response.data['message'], 'Empresa creada correctamente')

    def test_create_company_duplicate_rut(self):
        """
        Prueba la creación de una empresa con un RUT duplicado.
        """
        # Crear una empresa con un RUT específico
        Company.objects.create(com_rut='12345678-9', com_name_company='Empresa Existente', com_rut_representative='23456789-0', com_social_reason=1, com_twist_company='Servicios', com_address='Calle Falsa 123', country_id=1, region_id=1, commune_id=1, com_phone_one='123456789', com_mail_one='email@empresa.cl')

        # Intentar crear una nueva empresa con el mismo RUT
        response = self.client.post(reverse('post_company'), data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'La empresa ya existe')

    def test_invalid_rut_format(self):
        """
        Prueba la validación del formato de RUT.
        """
        invalid_data = self.valid_data.copy()
        invalid_data['com_rut'] = 'invalid-rut'
        response = self.client.post(reverse('post_company'), data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('com_rut', response.data)
        self.assertIn('El Rut ingresado no es válido', response.data['com_rut'])

    def test_create_company_with_parent(self):
        """
        Prueba la creación de una empresa con un ID de empresa padre.
        """
        parent_company = Company.objects.create(com_rut='87654321-0', com_name_company='Empresa Padre', com_rut_representative='34567890-1', com_social_reason=1, com_twist_company='Consultoría', com_address='Avenida Siempreviva 742', country_id=1, region_id=1, commune_id=1, com_phone_one='987654321', com_mail_one='padre@empresa.cl')

        self.valid_data['com_id_parent_company'] = parent_company.com_id
        response = self.client.post(reverse('post_company'), data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('com_id', response.data)
        self.assertEqual(response.data['message'], 'Empresa creada correctamente')

    def test_generic_error_handling(self):
        """
        Prueba el manejo de excepciones genéricas.
        """
        # Generar un error introduciendo datos incorrectos
        invalid_data = self.valid_data.copy()
        invalid_data['country'] = 'invalid-id'  # Esto debería lanzar una excepción
        response = self.client.post(reverse('post_company'), data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Error al crear la empresa')
