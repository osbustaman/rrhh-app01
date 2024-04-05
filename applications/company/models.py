from django.db import models

from applications.security.models import Country, Region, Commune


from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Create your models here.
class BoxesCompensation(models.Model):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    bc_id = models.AutoField("Key", primary_key=True)
    bc_name = models.CharField("Nombre", max_length=100)
    bc_code = models.CharField("Código", max_length=100)
    bc_rut = models.CharField("Rut", max_length=10)
    bc_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.bc_id

    def __str__(self):
        return f"{self.bc_name}"

    def save(self, *args, **kwargs):
        super(BoxesCompensation, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de cajas de compensación"
        db_table = "boxes_compensation"
        ordering = ['bc_id']


class MutualSecurity(models.Model):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    ms_id = models.AutoField("Key", primary_key=True)
    ms_name = models.CharField("Nombre", max_length=150)
    ms_rut = models.CharField("Rut", max_length=150)
    ms_codeprevired = models.CharField("Código Previred", max_length=10)
    ms_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.ms_id

    def __str__(self):
        return f"{self.ms_id} - {self.ms_name}"

    def save(self, *args, **kwargs):
        super(MutualSecurity, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de mutuales"
        db_table = "mutual_security"
        ordering = ['ms_id']


class Company(models.Model):
    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    BUSSINESS_SOCIAL_REASON = (
        (0, '( Seleccione )'),
        (1, 'Empresa Individual de Responsabilidad Limitada (E.I.R.L.)'),
        (2, 'Sociedad de Responsabilidad Limitada (S.R.L.)'),
        (3, 'Sociedad por Acciones (SpA)'),
        (4, 'Sociedad Anónima (S.A.)'),
        (5, 'Sociedad Anónima de Garantía Recíproca (S.A.G.R.)'),
    )


    com_id = models.AutoField("Key", primary_key=True)
    com_rut = models.CharField("Rut", max_length=25)
    com_representative_name = models.CharField(
        "Nombre representante", max_length=255, null=True, blank=True)
    com_rut_representative = models.CharField("Rut representante", max_length=25)
    com_is_state = models.CharField(
        "Es estatal", max_length=1, choices=OPTIONS, default="N")
    com_name_company = models.CharField("Nombre empresa", max_length=150)
    com_social_reason = models.IntegerField("Razón social", choices=BUSSINESS_SOCIAL_REASON)
    com_twist_company = models.CharField("Giro empresa", max_length=150)
    com_address = models.TextField("Dirección")
    com_department_office = models.CharField("Departamento/oficina", max_length=25, null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name="Country", db_column="com_country_id", on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name="Region", db_column="com_region_id", on_delete=models.PROTECT)
    commune = models.ForeignKey(Commune, verbose_name="Commune", db_column="com_commune_id", on_delete=models.PROTECT)
    com_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    com_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)
    com_zip_code = models.CharField("Código postal", max_length=25, null=True, blank=True)
    com_phone_one = models.CharField("Télefono 1", max_length=25)
    com_mail_one = models.CharField("Email 1", max_length=150)
    com_phone_two = models.CharField("Télefono 2", max_length=25, null=True, blank=True)
    com_mail_two = models.CharField("Email 2", max_length=150, null=True, blank=True)
    com_date_ingress = models.DateField(verbose_name='Fecha inicio de actividades', null=True, blank=True)
    com_is_holding = models.CharField("Es sub-empresa", max_length=1, choices=OPTIONS, default="S")
    com_id_parent_company = models.ForeignKey('self', db_column="com_id_parent_company", null=True, blank=True, default=None, on_delete=models.PROTECT)
    com_active = models.CharField("Empresa activa", max_length=1, choices=OPTIONS, default="S")
    com_rut_counter = models.CharField("Rut contador", max_length=12, null=True, blank=True)
    com_name_counter = models.CharField("Razón social", max_length=150, null=True, blank=True)
    com_company_image = models.CharField("Logo Empresa", max_length=255, null=True, blank=True)
    mutual_security = models.ForeignKey(MutualSecurity, verbose_name="MutualSecurity", db_column="com_mutualsecurity_id", on_delete=models.PROTECT, null=True, blank=True)
    boxes_compensation = models.ForeignKey(BoxesCompensation, verbose_name="BoxesCompensation", db_column="com_boxes_compensation_id", on_delete=models.PROTECT, null=True, blank=True)

    def __int__(self):
        return self.com_id

    def __str__(self):
        return f"{ self.com_id } - { self.com_name_company }"
    
    def __get_latitude_longitude(address):
        try:
            # Crear un objeto geolocator utilizando el proveedor Nominatim
            geolocator = Nominatim(user_agent="Nominatim", timeout=20)

            # Obtener la ubicación (latitud, longitud) a partir de la dirección
            location = geolocator.geocode(address)

            if location:
                latitude = location.latitude
                longitude = location.longitude
                return latitude, longitude
            else:
                print(f"No se pudo encontrar la ubicación para la dirección: {address}")
                return None, None
        except GeocoderTimedOut:
            print("El servicio de geocodificación excedió el tiempo de espera.")
            return None, None
        except Exception as e:
            print(f"Error al obtener la ubicación para la dirección {address}: {e}")
            return None, None
        
    get_latitude_longitude = property(__get_latitude_longitude)

    def save(self, *args, **kwargs):

        latitude, longitude = self.__get_latitude_longitude
        self.com_latitude = latitude
        self.com_longitude = longitude

        super(Company, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Empresas"
        db_table = 'company'
        ordering = ['com_id']


# Sucursal
class Subsidiary(models.Model):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    sub_id = models.AutoField("Key", primary_key=True)
    sub_name = models.CharField(
        "Descripción de la unidad", max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, verbose_name='Company', db_column='sub_company_id', on_delete=models.PROTECT)
    sub_address = models.CharField(
        "Direccion de la unidad", max_length=255, default='')
    country = models.ForeignKey(Country, verbose_name="Country",
                                db_column="sub_country_id", on_delete=models.PROTECT)
    region = models.ForeignKey(
        Region, verbose_name="Region", db_column="sub_region_id", on_delete=models.PROTECT)
    commune = models.ForeignKey(
        Commune, verbose_name="Commune", db_column="sub_commune_id", on_delete=models.PROTECT)
    sub_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    sub_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)
    sub_matrixhouse = models.CharField(
        "Es casa matriz", max_length=1, choices=OPTIONS, null=True, blank=True, default="N")
    sub_active = models.CharField(
        "Sucursal activa", max_length=1, choices=OPTIONS, default="S")

    def __int__(self):
        return self.sub_id

    def __str__(self):
        return f"{self.sub_name}"

    def __get_latitude_longitude(address):
        try:
            # Crear un objeto geolocator utilizando el proveedor Nominatim
            geolocator = Nominatim(user_agent="Nominatim", timeout=20)

            # Obtener la ubicación (latitud, longitud) a partir de la dirección
            location = geolocator.geocode(address)

            if location:
                latitude = location.latitude
                longitude = location.longitude
                return latitude, longitude
            else:
                print(f"No se pudo encontrar la ubicación para la dirección: {address}")
                return None, None
        except GeocoderTimedOut:
            print("El servicio de geocodificación excedió el tiempo de espera.")
            return None, None
        except Exception as e:
            print(f"Error al obtener la ubicación para la dirección {address}: {e}")
            return None, None
        
    get_latitude_longitude = property(__get_latitude_longitude)

    def save(self, *args, **kwargs):

        latitude, longitude = self.__get_latitude_longitude
        self.sub_latitude = latitude
        self.sub_longitude = longitude
        super(Subsidiary, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de sucursales"
        db_table = "subsidiary"
        ordering = ['sub_id']


# Cargo
class Position(models.Model):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    pos_id = models.AutoField("Key", primary_key=True)
    pos_name_position = models.CharField("Nombre cargo", max_length=255)
    company = models.ForeignKey(Company, verbose_name="Company",
                                db_column="pos_company_id", on_delete=models.PROTECT)
    pos_activa = models.CharField(
        "Cargo activa", max_length=1, choices=OPTIONS, default="S")
    
    def __int__(self):
        return self.pos_id

    def __str__(self):
        return f"{self.pos_name_position}"

    def save(self, *args, **kwargs):
        super(Position, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de cargos"
        db_table = 'position'
        ordering = ['pos_id']


class CenterCost(models.Model):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    cencost_id = models.AutoField("Key", primary_key=True)
    company = models.ForeignKey(Company, verbose_name="Company",
                                db_column="pos_company_id", on_delete=models.PROTECT)
    cencost_name = models.CharField("Nombre", max_length=100)
    cencost_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.cencost_id

    def __str__(self):
        return f"{self.cencost_name}"


    def save(self, *args, **kwargs):
        super(CenterCost, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de centros de costos"
        db_table = "center_cost"
        ordering = ['cencost_id']


class Health(models.Model):
    TIPO = (
        ('F', 'FONASA'),
        ('I', 'ISAPRE'),
    )

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    healt_id = models.AutoField("Key", primary_key=True)
    healt_name = models.CharField("Nombre", max_length=100)
    healt_code = models.CharField("Código", max_length=100)
    healt_entity_type = models.CharField("Tipo entidad", max_length=1, choices=TIPO, default='I')
    healt_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.healt_id

    def __str__(self):
        return f"{self.healt_name}"

    def __porcentaje_fonasa(self):
        if self.healt_entity_type == 'F':
            return 7
        else:
            return 0

    porcentajeFonasa = property(__porcentaje_fonasa)

    def save(self, *args, **kwargs):
        super(Health, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de entidades de salud"
        db_table = "health"
        ordering = ['healt_id']


class Afp(models.Model):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )
    
    afp_id = models.AutoField("Key", primary_key=True)
    afp_code_previred = models.CharField("Código previred", max_length=100, null=False, blank=True)
    afp_name = models.CharField("Nombre", max_length=100)
    afp_dependent_worker_rate = models.FloatField(
        "Tasa traba. dependiente", default=0)
    afp_sis = models.FloatField(
        "Seguro de Invalidez y Sobrevivencia (SIS)", default=0)
    afp_self_employed_worker_rate = models.FloatField(
        "Tasa traba. independiente", default=0)
    afp_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="T")

    def __int__(self):
        return self.afp_id

    def __str__(self):
        return f"{self.afp_code_previred} - {self.afp_name}"

    def save(self, *args, **kwargs):
        super(Afp, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de entidades afp"
        db_table = "afp"
        ordering = ['afp_id']


class Apv(models.Model):

    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    apv_id = models.AutoField("Key", primary_key=True)
    apv_code_previred = models.CharField("Código previred", max_length=100, null=True, blank=True)
    apv_name = models.CharField("Nombre", max_length=100)
    apv_name_company_reason = models.CharField(
        "Nombre razón social", max_length=150, null=True, blank=True)
    apv_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.apv_id

    def __str__(self):
        return f"{self.apv_name}"

    def save(self, *args, **kwargs):
        super(Apv, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de entidades apv"
        db_table = "apv"
        ordering = ['apv_id']


class Bank(models.Model):
    OPTIONS = (
        ('Y', 'SI'),
        ('N', 'NO'),
    )

    ban_id = models.AutoField("Key", primary_key=True)
    ban_name = models.CharField("Nombre del banco", max_length=150)
    ban_code = models.CharField("Código", max_length=10)
    ban_active = models.CharField(
        "Activo", max_length=1, choices=OPTIONS, default="Y")

    def __int__(self):
        return self.ban_id

    def __str__(self):
        return f"{self.ban_name}"

    def save(self, *args, **kwargs):
        super(Bank, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de bancos"
        db_table = "banks"
        ordering = ['ban_id']