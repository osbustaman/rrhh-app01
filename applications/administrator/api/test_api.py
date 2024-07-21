import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from applications.security.models import Country, Region, Commune, Customers
from applications.administrator.api.serializer import (
    CustomerSerializer,
    CommuneSerializer,
    RegionSerializer,
    UserSerializer,
    CountriesSerializer,
)


class ListCountriesViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("list-countries")

    def test_list_countries(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Country.objects.count())


class ListRegionViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("list-regions")

    def test_list_regions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Region.objects.count())


class ListCommuneViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("list-communes")

    def test_list_communes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Commune.objects.count())


class CreateCustomerViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("create-customer")
        self.valid_payload = {
            "cus_name": "Test Customer",
            "cus_identifier": "123456789",
            "cus_email": "test@example.com",
            "cus_representative_name": "John Doe",
            "cus_representative_rut": "987654321",
            "cus_representative_mail": "john.doe@example.com",
            "cus_name_bd": "Test DB",
            "cus_date_in": "2022-01-01",
            "cus_date_out": "2022-12-31",
            "cus_number_users": 10,
            "country_id": 1,
            "region_id": 1,
            "commune_id": 1,
        }

    def test_create_customer(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customers.objects.count(), 1)


class ListCustomersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("list-customers")

    def test_list_customers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Customers.objects.filter(cus_active="Y").count())


class ListAdminUsersViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("list-admin-users")
        self.user = User.objects.create_user(username="admin", password="admin123", is_staff=True, is_superuser=True)

    def test_list_admin_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["users"]), User.objects.filter(is_staff=True, is_superuser=True).count())


class CreateUserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("create-user")
        self.user = User.objects.create_user(username="admin", password="admin123", is_staff=True, is_superuser=True)
        self.valid_payload = {
            "database_name": "test_db",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "test123",
        }

    def test_create_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.using("test_db").count(), 1)