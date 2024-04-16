import django
import os
import psycopg2

from decouple import config
from django.db import models, IntegrityError
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command

from model_utils.models import TimeStampedModel
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from unidecode import unidecode

# Create your models here.


class Country(TimeStampedModel):

    cou_id = models.AutoField("Key", primary_key=True)
    cou_name = models.CharField("Nombre país", max_length=255)
    cou_code = models.IntegerField("Código area país", unique=True)

    def __int__(self):
        return self.cou_id

    def __str__(self):
        return f"{self.cou_name}"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de paises"
        db_table = 'country'
        ordering = ['cou_id']


class Region(TimeStampedModel):

    re_id = models.AutoField("Key", primary_key=True)
    re_name = models.CharField("Nombre región", max_length=255)
    country_id = models.ForeignKey(Country, verbose_name="Country", on_delete=models.PROTECT, db_column="country_id")
    re_region_acronym = models.CharField(
        "Sigla de región", blank=True, null=True, max_length=5)
    re_number = models.IntegerField("Número de región", db_index=True)

    def __int__(self):
        return self.re_id

    def __str__(self):
        return f"{self.re_name}"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Region, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de regiones"
        db_table = 'regions'
        ordering = ['re_id']


class Commune(TimeStampedModel):
    com_id = models.AutoField("Key", primary_key=True)
    com_name = models.CharField("Nombre comuna", max_length=255)
    com_number = models.IntegerField("Numero comuna", default=0)
    region_id = models.ForeignKey(Region, verbose_name="Region", on_delete=models.PROTECT, db_column="region_id")

    def __int__(self):
        return self.com_id

    def __str__(self):
        return f"{self.com_name}"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(Commune, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de comunas"
        db_table = 'communes'
        ordering = ['com_id']


class Menu(TimeStampedModel):

    ACTIVE = (
        ("Y", "YES"),
        ("N", "NO")
    )

    m_id = models.AutoField("Key", primary_key=True)
    m_user = models.ForeignKey(User, verbose_name="Colaborador",
                             db_column="m_user_id",  on_delete=models.PROTECT)
    m_name = models.CharField("Nombre Menú", max_length=100)
    m_active = models.CharField("Activo", max_length=1, choices=ACTIVE, default="Y")

    def __int__(self):
        return self.ee_id

    def __str__(self):
        return f"{self.m_id} - {self.m_user}"

    def save(self, *args, **kwargs):
        super(Menu, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de Menus"
        db_table = "menu"
        ordering = ['m_id']


class ListItems(TimeStampedModel):

    ACTIVE = (
        ("Y", "YES"),
        ("N", "NO")
    )

    li_id = models.AutoField("Key", primary_key=True)
    li_name = models.CharField("Nombre Menú", max_length=100)
    li_short_name = models.CharField("Nombre Corto", max_length=100, null=True, blank=True)
    li_order = models.IntegerField("Posición del item", null=True, blank=True)
    li_icon= models.CharField("Icono Menú", max_length=100, default="beer")
    li_active = models.CharField("Activo", max_length=1, choices=ACTIVE, default="Y")

    def __int__(self):
        return self.li_id

    def __str__(self):
        return f"{self.li_id} - {self.li_name}"

    def __create_short_name(self):
        return (self.li_name).lower().replace(" ", "_")

    def __remove_accent(self, value):
        return unidecode(value)

    def __order_more_one(self):
        last_element = ListItems.objects.filter(li_active="Y")

        if last_element.filter(li_id = self.li_id):
            return self.li_order
        else:
            num_order = last_element.last().li_order
            return num_order + 1 if num_order > 0 else 0

    create_short_name = property(__create_short_name)
    order_more_one = property(__order_more_one)
    remove_accent = property(__remove_accent)

    def save(self, *args, **kwargs):
        self.li_short_name = self.__remove_accent(self.create_short_name)
        self.li_order = self.order_more_one
        super(ListItems, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de Items"
        db_table = "items"
        ordering = ['li_id']


class MenuItems(TimeStampedModel):

    ACTIVE = (
        ("Y", "YES"),
        ("N", "NO")
    )

    mi_menu = models.ForeignKey(Menu, verbose_name="Menu",
                             db_column="mi_menu_id", on_delete=models.PROTECT)
    mi_items = models.ForeignKey(ListItems, verbose_name="Items",
                             db_column="mi_items_id", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.mi_menu} - {self.mi_items}"

    def save(self, *args, **kwargs):
        super(MenuItems, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Menus y sus Items"
        db_table = "menu_items"
        ordering = ['mi_menu__m_id', 'mi_items__li_id']


class ListSubItems(TimeStampedModel):

    ACTIVE = (
        ("Y", "YES"),
        ("N", "NO")
    )

    lsi_id = models.AutoField("Key", primary_key=True)
    lsi_name = models.CharField("Nombre SubItem", max_length=100)
    lsi_short_name = models.CharField("Nombre Corto", max_length=100, null=True, blank=True)
    lsi_order = models.IntegerField("Posición del SubItem", null=True, blank=True)
    lsi_url= models.TextField("Url", default="#")
    lsi_items = models.ForeignKey(ListItems, verbose_name="Items",
                            db_column="lsi_items_id", on_delete=models.PROTECT)
    lsi_active = models.CharField("Activo", max_length=1, choices=ACTIVE, default="Y")

    def __int__(self):
        return self.lsi_id

    def __str__(self):
        return f"{self.lsi_id} - {self.lsi_items}"

    def __create_short_name(self):
        return (self.lsi_name).lower().replace(" ", "_")

    def __remove_accent(self, value):
        return unidecode(value)

    def __order_more_one(self):
        last_element = ListSubItems.objects.filter(lsi_active="Y")

        if last_element.filter(lsi_id = self.lsi_id):
            return self.lsi_order
        else:
            num_order = last_element.last().lsi_order
            return num_order + 1 if num_order > 0 else 0

    create_short_name = property(__create_short_name)
    order_more_one = property(__order_more_one)
    remove_accent = property(__remove_accent)

    def save(self, *args, **kwargs):
        self.lsi_short_name = self.__remove_accent(self.create_short_name)
        self.lsi_order = self.order_more_one
        super(ListSubItems, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de Sub Items"
        db_table = "list_sub_items"
        ordering = ['lsi_id']


class Customers(TimeStampedModel):

    ACTIVE = (
        ("Y", "YES"),
        ("N", "NO")
    )

    cus_id = models.AutoField("Key", primary_key=True)
    cus_name = models.CharField('Nombre del cliente', max_length=120)
    cus_identifier = models.CharField('Rut del cliente', max_length=20)
    cus_name_bd = models.CharField('Nombre base de datos', max_length=20, null=True, blank=True)
    cus_date_in = models.DateField("Fecha creación de la base")
    cus_date_out = models.DateField(verbose_name='Fecha termino de la base', null=True, blank=True)

    cus_link = models.CharField("Link base", max_length=255, null=True, blank=True)
    cus_client_image = models.ImageField(
        "Logo Cliente", help_text=" Formatos .jpg|.png|.gif|.jpeg", upload_to='imagen/', null=True, blank=True)
    
    cus_client_favicon = models.ImageField(
        "Favicon Cliente", help_text=" Formatos .jpg|.png|.gif|.jpeg", upload_to='imagen/', null=True, blank=True)
    
    cus_number_users = models.IntegerField("Cantidad usuarios", default=0, null=True, blank=True)
    cus_representative_rut = models.CharField("Rut representante", max_length=20, null=True, blank=True)
    cus_representative_mail = models.CharField("Rut representante", max_length=100, null=True, blank=True)
    cus_representative_phone = models.CharField("Teléfono representante", max_length=100, null=True, blank=True)
    cus_representative_address = models.CharField("Dirección representante", max_length=100, null=True, blank=True)
    country_id = models.ForeignKey(Country, verbose_name="Country", db_column="country_id", null=True, blank=True, on_delete=models.PROTECT)
    region_id = models.ForeignKey(Region, verbose_name="Region", db_column="region_id", null=True, blank=True, on_delete=models.PROTECT)
    commune_id = models.ForeignKey(Commune, verbose_name="Commune", db_column="commune_id", null=True, blank=True, on_delete=models.PROTECT)
    cus_zip_code = models.CharField("Código postal", max_length=25, null=True, blank=True)
    cus_directory_path = models.CharField("Directorio cliente", max_length=255, null=True, blank=True)
    cus_active = models.CharField("Activo", max_length=1, choices=ACTIVE, default="Y")

    def __int__(self):
        return self.cus_id

    def __str__(self):
        return f"{self.cus_id} - {self.cus_name}"

    def __create_name_db(self):
        return (self.cus_name).replace(" ", "_").lower()

    def __link_customer(self):
        return f"/{self.cus_name_bd.lower()}/"

    def __create_database(self):
        try:
            # Conexión a la base de datos PostgreSQL
            connection = psycopg2.connect(
                dbname='postgres',
                user=settings.DATABASES['default']['USER'],
                host=settings.DATABASES['default']['HOST'],
                password=settings.DATABASES['default']['PASSWORD']
            )
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False

        # Cursor para ejecutar consultas
        cursor = connection.cursor()

        try:
            # Verificar si la base de datos existe
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.cus_name_bd}'")
            exists = cursor.fetchone()
            if not exists:
                # Crear la base de datos si no existe
                cursor.execute(f"CREATE DATABASE {self.cus_name_bd}")
                print(f"Base de datos {self.cus_name_bd} creada exitosamente.")
        except psycopg2.Error as e:
            print(f"Error al crear la base de datos: {e}")
        finally:
            # Cerrar la conexión y el cursor
            cursor.close()
            connection.close()


        return True


    def __create_migrate(self):
        try:
            # Configurar el entorno de Django
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "remunerations.settings.local")
            django.setup()

            # Definir los parámetros para la nueva base de datos
            nueva_base = {
                'ENGINE': settings.DATABASES['default']['ENGINE'],
                'HOST': config('HOST'),
                'NAME': self.cus_name_bd,
                'USER': config('USER'),
                'PASSWORD': config('PASSWORD'),
                'PORT': config('PORT')
            }

            # Configurar la nueva base de datos en las configuraciones de Django
            settings.DATABASES[self.cus_name_bd] = nueva_base

            # Ejecutar las migraciones en la nueva base de datos
            call_command('migrate', database=self.cus_name_bd)

            # Devolver un mensaje indicando que no hay errores
            return "Las migraciones se han completado correctamente."
        except django.core.exceptions.ImproperlyConfigured as e:
            # Manejar el error de configuración de Django
            return f'Error de configuración de Django: {e}'
        except django.db.utils.OperationalError as e:
            # Manejar el error de conexión con el servidor de la base de datos
            return f'Error al conectar con el servidor de la base de datos: {e}'
        except Exception as e:
            # Manejar cualquier otro error desconocido
            return f'Error desconocido: {e}'


    def __populate_customer_base_country(self):
        try:
            # Verificar si el país ya existe en la base de datos del cliente
            country = Country.objects.using(self.cus_name_bd).get(cou_code=56)
        except Country.DoesNotExist:
            # Si no existe, crear el país
            country = Country(cou_name='Chile', cou_code=56)
            try:
                country.save(using=self.cus_name_bd)
            except IntegrityError:
                # En caso de que haya un error de integridad, se supone que el país ya existe, 
                # se realiza otra consulta para obtenerlo
                country = Country.objects.using(self.cus_name_bd).get(cou_code=56)
        except Exception as e:
            # Manejar cualquier otro error que pueda ocurrir
            print(f"Error al poblar la base de datos del cliente: {e}")
            return None

        return country
    
    populate_customer_base_country = property(__populate_customer_base_country)
    
    def __populate_customer_base_regions_and_comunnes(self):

        list_regions = [{
            're_name': 'Tarapacá',
            're_region_number': 'I',
            're_number': 1,
            'comunnes': [
                {'com_name': 'Iquique'},
                {'com_name': 'Alto Hospicio'},
                {'com_name': 'Pozo Almonte'},
                {'com_name': 'Camiña'},
                {'com_name': 'Colchane'},
                {'com_name': 'Huara'},
                {'com_name': 'Pica'},
            ]
        }, {
            're_name': 'Antofagasta',
            're_region_number': 'II',
            're_number': 2,
            'comunnes': [
                {'com_name': 'Antofagasta'},
                {'com_name': 'Mejillones'},
                {'com_name': 'Sierra Gorda'},
                {'com_name': 'Taltal'},
                {'com_name': 'Calama'},
                {'com_name': 'Ollagüe'},
                {'com_name': 'San Pedro de Atacama'},
                {'com_name': 'Tocopilla'},
                {'com_name': 'María Elena'},

            ]
        }, {
            're_name': 'Atacama',
            're_region_number': 'III',
            're_number': 3,
            'comunnes': [
                {'com_name': 'Copiapó'},
                {'com_name': 'Caldera'},
                {'com_name': 'Tierra Amarilla'},
                {'com_name': 'Chañaral'},
                {'com_name': 'Diego de Almagro'},
                {'com_name': 'Vallenar'},
                {'com_name': 'Alto del Carmen'},
                {'com_name': 'Freirina'},
                {'com_name': 'Huasco'},

            ]
        }, {
            're_name': 'Coquimbo',
            're_region_number': 'IV',
            're_number': 4,
            'comunnes': [
                {'com_name': 'Huasco'},
                {'com_name': 'La Serena'},
                {'com_name': 'Coquimbo'},
                {'com_name': 'Andacollo'},
                {'com_name': 'La Higuera'},
                {'com_name': 'Paiguano'},
                {'com_name': 'Vicuña'},
                {'com_name': 'Illapel'},
                {'com_name': 'Canela'},
                {'com_name': 'Los Vilos'},
                {'com_name': 'Salamanca'},
                {'com_name': 'Ovalle'},
                {'com_name': 'Combarbalá'},
                {'com_name': 'Monte Patria'},
                {'com_name': 'Punitaqui'},
                {'com_name': 'Río Hurtado'},

            ]
        }, {
            're_name': 'Valparaiso',
            're_region_number': 'V',
            're_number': 5,
            'comunnes': [
                {'com_name': 'Río Hurtado'},
                {'com_name': 'Valparaíso'},
                {'com_name': 'Casablanca'},
                {'com_name': 'Concón'},
                {'com_name': 'Juan Fernández'},
                {'com_name': 'Puchuncaví'},
                {'com_name': 'Quilpué'},
                {'com_name': 'Quintero'},
                {'com_name': 'Villa Alemana'},
                {'com_name': 'Viña del Mar'},
                {'com_name': 'Isla de Pascua'},
                {'com_name': 'Los Andes'},
                {'com_name': 'Calle Larga'},
                {'com_name': 'Rinconada'},
                {'com_name': 'San Esteban'},
                {'com_name': 'La Ligua'},
                {'com_name': 'Cabildo'},
                {'com_name': 'Papudo'},
                {'com_name': 'Petorca'},
                {'com_name': 'Zapallar'},
                {'com_name': 'Quillota'},
                {'com_name': 'Calera'},
                {'com_name': 'Hijuelas'},
                {'com_name': 'La Cruz'},
                {'com_name': 'Limache'},
                {'com_name': 'Nogales'},
                {'com_name': 'Olmué'},
                {'com_name': 'San Antonio'},
                {'com_name': 'Algarrobo'},
                {'com_name': 'Cartagena'},
                {'com_name': 'El Quisco'},
                {'com_name': 'El Tabo'},
                {'com_name': 'Santo Domingo'},
                {'com_name': 'San Felipe'},
                {'com_name': 'Catemu'},
                {'com_name': 'Llaillay'},
                {'com_name': 'Panquehue'},
                {'com_name': 'Putaendo'},
                {'com_name': 'Santa María'},

            ]
        }, {
            're_name': 'Metropolitana de Santiago',
            're_region_number': 'RM',
            're_number': 13,
            'comunnes': [
                {'com_name': 'Santiago'},
                {'com_name': 'Cerrillos'},
                {'com_name': 'Cerro Navia'},
                {'com_name': 'Conchalí'},
                {'com_name': 'El Bosque'},
                {'com_name': 'Estación Central '},
                {'com_name': 'Huechuraba'},
                {'com_name': 'Independencia'},
                {'com_name': 'La Cisterna'},
                {'com_name': 'La Florida'},
                {'com_name': 'La Pintana'},
                {'com_name': 'La Granja'},
                {'com_name': 'La Reina'},
                {'com_name': 'Las Condes'},
                {'com_name': 'Lo Barnechea'},
                {'com_name': 'Lo Espejo'},
                {'com_name': 'Lo Prado'},
                {'com_name': 'Macul'},
                {'com_name': 'Maipú'},
                {'com_name': 'Ñuñoa'},
                {'com_name': 'Pedro Aguirre Cerda'},
                {'com_name': 'Peñalolén'},
                {'com_name': 'Providencia'},
                {'com_name': 'Pudahuel'},
                {'com_name': 'Quilicura'},
                {'com_name': 'Quinta Normal'},
                {'com_name': 'Recoleta'},
                {'com_name': 'Renca'},
                {'com_name': 'San Joaquín'},
                {'com_name': 'San Miguel'},
                {'com_name': 'San Ramón'},
                {'com_name': 'Vitacura'},
                {'com_name': 'Puente Alto'},
                {'com_name': 'Pirque'},
                {'com_name': 'San José de Maipo'},
                {'com_name': 'Colina'},
                {'com_name': 'Lampa'},
                {'com_name': 'Tiltil'},
                {'com_name': 'San Bernardo'},
                {'com_name': 'Buin'},
                {'com_name': 'Calera de Tango'},
                {'com_name': 'Paine'},
                {'com_name': 'Melipilla'},
                {'com_name': 'Alhué'},
                {'com_name': 'Curacaví'},
                {'com_name': 'María Pinto'},
                {'com_name': 'San Pedro'},
                {'com_name': 'Talagante'},
                {'com_name': 'El Monte'},
                {'com_name': 'Isla de Maipo'},
                {'com_name': 'Padre Hurtado'},
                {'com_name': 'Peñaflor'},

            ]
        }, {
            're_name': 'Libertador General Bernardo O\'Higgins',
            're_region_number': 'VI',
            're_number': 6,
            'comunnes': [
                {'com_name': 'Rancagua'},
                {'com_name': 'Codegua'},
                {'com_name': 'Coinco'},
                {'com_name': 'Coltauco'},
                {'com_name': 'Doñihue'},
                {'com_name': 'Graneros'},
                {'com_name': 'Las Cabras'},
                {'com_name': 'Machalí'},
                {'com_name': 'Malloa'},
                {'com_name': 'Mostazal'},
                {'com_name': 'Olivar'},
                {'com_name': 'Peumo'},
                {'com_name': 'Pichidegua'},
                {'com_name': 'Quinta de Tilcoco'},
                {'com_name': 'Rengo'},
                {'com_name': 'Requínoa'},
                {'com_name': 'San Vicente'},
                {'com_name': 'Pichilemu'},
                {'com_name': 'La Estrella'},
                {'com_name': 'Litueche'},
                {'com_name': 'Marchihue'},
                {'com_name': 'Navidad'},
                {'com_name': 'Paredones'},
                {'com_name': 'San Fernando'},
                {'com_name': 'Chépica'},
                {'com_name': 'Chimbarongo'},
                {'com_name': 'Lolol'},
                {'com_name': 'Nancagua'},
                {'com_name': 'Palmilla'},
                {'com_name': 'Peralillo'},
                {'com_name': 'Placilla'},
                {'com_name': 'Pumanque'},
                {'com_name': 'Santa Cruz'},
            ]
        }, {
            're_name': 'Maule',
            're_region_number': 'VII',
            're_number': 7,
            'comunnes': [
                {'com_name': 'Talca'},
                {'com_name': 'Constitución'},
                {'com_name': 'Curepto'},
                {'com_name': 'Empedrado'},
                {'com_name': 'Maule'},
                {'com_name': 'Pelarco'},
                {'com_name': 'Pencahue'},
                {'com_name': 'Río Claro'},
                {'com_name': 'San Clemente'},
                {'com_name': 'San Rafael'},
                {'com_name': 'Cauquenes'},
                {'com_name': 'Chanco'},
                {'com_name': 'Pelluhue'},
                {'com_name': 'Curicó'},
                {'com_name': 'Hualañé'},
                {'com_name': 'Licantén'},
                {'com_name': 'Molina'},
                {'com_name': 'Rauco'},
                {'com_name': 'Romeral'},
                {'com_name': 'Sagrada Familia'},
                {'com_name': 'Teno'},
                {'com_name': 'Vichuquén'},
                {'com_name': 'Linares'},
                {'com_name': 'Colbún'},
                {'com_name': 'Longaví'},
                {'com_name': 'Parral'},
                {'com_name': 'Retiro'},
                {'com_name': 'San Javier'},
                {'com_name': 'Villa Alegre'},
                {'com_name': 'Yerbas Buenas'},
            ]
        }, {
            're_name': 'Biobío',
            're_region_number': 'VIII',
            're_number': 8,
            'comunnes': [
                {'com_name': 'Concepción'},
                {'com_name': 'Coronel'},
                {'com_name': 'Chiguayante'},
                {'com_name': 'Florida'},
                {'com_name': 'Hualqui'},
                {'com_name': 'Lota'},
                {'com_name': 'Penco'},
                {'com_name': 'San Pedro de la Paz'},
                {'com_name': 'Santa Juana'},
                {'com_name': 'Talcahuano'},
                {'com_name': 'Tomé'},
                {'com_name': 'Hualpén'},
                {'com_name': 'Lebu'},
                {'com_name': 'Arauco'},
                {'com_name': 'Cañete'},
                {'com_name': 'Contulmo'},
                {'com_name': 'Curanilahue'},
                {'com_name': 'Los Álamos'},
                {'com_name': 'Tirúa'},
                {'com_name': 'Los Ángeles'},
                {'com_name': 'Antuco'},
                {'com_name': 'Cabrero'},
                {'com_name': 'Laja'},
                {'com_name': 'Mulchén'},
                {'com_name': 'Nacimiento'},
                {'com_name': 'Negrete'},
                {'com_name': 'Quilaco'},
                {'com_name': 'Quilleco'},
                {'com_name': 'San Rosendo'},
                {'com_name': 'Santa Bárbara'},
                {'com_name': 'Tucapel'},
                {'com_name': 'Yumbel'},
                {'com_name': 'Alto Bío-Bío'},
                {'com_name': 'Chillán'},
                {'com_name': 'Bulnes'},
                {'com_name': 'Cobquecura'},
                {'com_name': 'Coelemu'},
                {'com_name': 'Coihueco'},
                {'com_name': 'Chillán Viejo'},
                {'com_name': 'El Carmen'},
                {'com_name': 'Ninhue'},
                {'com_name': 'Ñiquén'},
                {'com_name': 'Pemuco'},
                {'com_name': 'Pinto'},
                {'com_name': 'Portezuelo'},
                {'com_name': 'Quillón'},
                {'com_name': 'Quirihue'},
                {'com_name': 'Ránquil'},
                {'com_name': 'San Carlos'},
                {'com_name': 'San Fabián'},
                {'com_name': 'San Ignacio'},
                {'com_name': 'San Nicolás'},
                {'com_name': 'Treguaco'},
                {'com_name': 'Yungay'},
            ]
        }, {
            're_name': 'La Araucanía',
            're_region_number': 'IX',
            're_number': 9,
            'comunnes': [
                {'com_name': 'Temuco'},
                {'com_name': 'Carahue'},
                {'com_name': 'Cunco'},
                {'com_name': 'Curarrehue'},
                {'com_name': 'Freire'},
                {'com_name': 'Galvarino'},
                {'com_name': 'Gorbea'},
                {'com_name': 'Lautaro'},
                {'com_name': 'Loncoche'},
                {'com_name': 'Melipeuco'},
                {'com_name': 'Nueva Imperial'},
                {'com_name': 'Padre las Casas'},
                {'com_name': 'Perquenco'},
                {'com_name': 'Pitrufquén'},
                {'com_name': 'Pucón'},
                {'com_name': 'Saavedra'},
                {'com_name': 'Teodoro Schmidt'},
                {'com_name': 'Toltén'},
                {'com_name': 'Vilcún'},
                {'com_name': 'Villarrica'},
                {'com_name': 'Cholchol'},
                {'com_name': 'Angol'},
                {'com_name': 'Collipulli'},
                {'com_name': 'Curacautín'},
                {'com_name': 'Ercilla'},
                {'com_name': 'Lonquimay'},
                {'com_name': 'Los Sauces'},
                {'com_name': 'Lumaco'},
                {'com_name': 'Purén'},
                {'com_name': 'Renaico'},
                {'com_name': 'Traiguén'},
                {'com_name': 'Victoria'},
            ]
        }, {
            're_name': 'Los Lagos',
            're_region_number': 'X',
            're_number': 10,
            'comunnes': [
                {'com_name': 'Puerto Montt'},
                {'com_name': 'Calbuco'},
                {'com_name': 'Cochamó'},
                {'com_name': 'Fresia'},
                {'com_name': 'Frutillar'},
                {'com_name': 'Los Muermos'},
                {'com_name': 'Llanquihue'},
                {'com_name': 'Maullín'},
                {'com_name': 'Puerto Varas'},
                {'com_name': 'Castro'},
                {'com_name': 'Ancud'},
                {'com_name': 'Chonchi'},
                {'com_name': 'Curaco de Vélez'},
                {'com_name': 'Dalcahue'},
                {'com_name': 'Puqueldón'},
                {'com_name': 'Queilén'},
                {'com_name': 'Quellón'},
                {'com_name': 'Quemchi'},
                {'com_name': 'Quinchao'},
                {'com_name': 'Osorno'},
                {'com_name': 'Puerto Octay'},
                {'com_name': 'Purranque'},
                {'com_name': 'Puyehue'},
                {'com_name': 'Río Negro'},
                {'com_name': 'San Juan de La Costa'},
                {'com_name': 'San Pablo'},
                {'com_name': 'Chaitén'},
                {'com_name': 'Futaleufú'},
                {'com_name': 'Hualaihué'},
                {'com_name': 'Palena'},
            ]
        }, {
            're_name': 'Aisén del General Carlos Ibáñez del Campo',
            're_region_number': 'XI',
            're_number': 11,
            'comunnes': [
                {'com_name': 'Coihaique'},
                {'com_name': 'Lago Verde'},
                {'com_name': 'Aysen'},
                {'com_name': 'Cisnes'},
                {'com_name': 'Guaitecas'},
                {'com_name': 'Cochrane'},
                {'com_name': 'O\'Higgins'},
                {'com_name': 'Tortel'},
                {'com_name': 'Chile Chico'},
                {'com_name': 'Río Ibáñez'},
            ]
        }, {
            're_name': 'Magallanes y de la Antártica Chilena',
            're_region_number': 'XII',
            're_number': 12,
            'comunnes': [
                {'com_name': 'Punta Arenas'},
                {'com_name': 'Laguna Blanca'},
                {'com_name': 'Río Verde'},
                {'com_name': 'San Gregorio'},
                {'com_name': 'Cabo de Hornos'},
                {'com_name': 'Antártica'},
                {'com_name': 'Porvenir'},
                {'com_name': 'Primavera'},
                {'com_name': 'Timaukel'},
                {'com_name': 'Natales'},
                {'com_name': 'Torres del Paine'},
            ]
        }, {
            're_name': 'Los Ríos',
            're_region_number': 'XIV',
            're_number': 14,
            'comunnes': [
                {'com_name': 'Valdivia'},
                {'com_name': 'Corral'},
                {'com_name': 'Lanco'},
                {'com_name': 'Los Lagos'},
                {'com_name': 'Máfil'},
                {'com_name': 'Mariquina'},
                {'com_name': 'Paillaco'},
                {'com_name': 'Panguipulli'},
                {'com_name': 'La Unión'},
                {'com_name': 'Futrono'},
                {'com_name': 'Lago Ranco'},
                {'com_name': 'Río Bueno'},
            ]
        }, {
            're_name': 'Arica y Parinacota',
            're_region_number': 'XV',
            're_number': 15,
            'comunnes': [
                {'com_name': 'Arica'},
                {'com_name': 'Camarones'},
                {'com_name': 'Putre'},
                {'com_name': 'General Lagos'},
            ]
        }]

        for lr in list_regions:
            try:
                # Verificar si la región ya existe en la base de datos del cliente
                region = Region.objects.using(self.cus_name_bd).get(re_number=lr['re_number'])
            except Region.DoesNotExist:
                # Si no existe, crear la región
                region = Region(
                    re_name=lr['re_name'],
                    country_id=Country.objects.using(self.cus_name_bd).get(cou_code=56),  # Llamada a una función para obtener el país
                    re_region_acronym=lr['re_region_number'],
                    re_number=lr['re_number']
                )
                region.save(using=self.cus_name_bd)

                # Crear comunas para la región
                for c in lr['comunnes']:
                    commune = Commune(com_name=c['com_name'], region_id=region)
                    commune.save(using=self.cus_name_bd)
            except Exception as e:
                print(f"Error al poblar la base de datos del cliente con las regiones y comunas: {e}")
                return False

        return True
    
    def __create_boxes_compensation(self):
        
        from applications.company.models import BoxesCompensation

        list_boxes = [
                        {
                            "bc_rut": "81826800-9",
                            "bc_business_name": "CAJA DE COMPENSACION DE ASIGNACION FAMILIAR DE LOS ANDES",
                            "bc_fantasy_name": "CCAF LOS ANDES",
                            "bc_phone": "225100374",
                            "bc_email": "N/A",
                            "bc_address": "CALLE GENERAL CALDERON 121",
                            "region": "Metropolitana de Santiago",
                            "commune": "Providencia",
                        }, {
                            "bc_rut": "70016160-9",
                            "bc_business_name": "CAJA DE COMPENSACION DE ASIGNACION FAMILIAR LA ARAUCANA",
                            "bc_fantasy_name": "CCAF LA ARAUCANA",
                            "bc_phone": "4228252",
                            "bc_email": "ggeneral@laaraucana.cl",
                            "bc_address": "MERCED 472",
                            "region": "Metropolitana de Santiago",
                            "commune": "Santiago",
                        }, {
                            "bc_rut": "70016330-K",
                            "bc_business_name": "CAJA DE COMPENSACION DE ASIGNACION FAMILIAR LOS HEROES",
                            "bc_fantasy_name": "CCAF LOS HEROES",
                            "bc_phone": "7296260",
                            "bc_email": "N/A",
                            "bc_address": "AV. HOLANDA 64",
                            "region": "Metropolitana de Santiago",
                            "commune": "Providencia",
                        }
                    ]

        for box_data in list_boxes:

            # Verificar si el registro ya existe
            if not BoxesCompensation.objects.using(self.cus_name_bd).filter(bc_rut=box_data['bc_rut']).exists():
                
                region_name = box_data.pop("region")
                commune_name = box_data.pop("commune") 
                
                region_instance = Region.objects.using(self.cus_name_bd).get(re_name=region_name)
                commune_instance = Commune.objects.using(self.cus_name_bd).get(com_name=commune_name, region_id=region_instance)   
                
                BoxesCompensation.objects.using(self.cus_name_bd).create(
                    region=region_instance,
                    commune=commune_instance,
                    **box_data
                )

    def __create_banks(self):

        from applications.company.models import Bank

        list_banks = [
            {
                "ban_name": "BANCO DE CHILE",
                "ban_code": "001"
            }, {
                "ban_name": "BANCO INTERNACIONAL",
                "ban_code": "009"
            }, {
                "ban_name": "SCOTIABANK CHILE",
                "ban_code": "014"
            }, {
                "ban_name": "BANCO DE CREDITO E INVERSIONES",
                "ban_code": "016"
            }, {
                "ban_name": "BANCO BICE",
                "ban_code": "028"
            }, {
                "ban_name": "HSBC BANK (CHILE)",
                "ban_code": "031"
            }, {
                "ban_name": "BANCO SANTANDER-CHILE",
                "ban_code": "037"
            }, {
                "ban_name": "BANCO ITAÚ CHILE",
                "ban_code": "039"
            }, {
                "ban_name": "BANCO SECURITY",
                "ban_code": "049"
            }, {
                "ban_name": "BANCO FALABELLA",
                "ban_code": "051"
            }, {
                "ban_name": "BANCO RIPLEY",
                "ban_code": "053"
            }, {
                "ban_name": "BANCO CONSORCIO",
                "ban_code": "055"
            }, {
                "ban_name": "BANCO BTG PACTUAL CHILE",
                "ban_code": "059"
            }
        ]

        for bank_data in list_banks:

            # Verificar si el registro ya existe
            if not Bank.objects.using(self.cus_name_bd).filter(ban_code=bank_data['ban_code']).exists():

                bank_name = bank_data.pop("ban_name")
                bank_code = bank_data.pop("ban_code")

                Bank.objects.using(self.cus_name_bd).create(
                    ban_name=bank_name,
                    ban_code=bank_code,
                )

    def __create_afp(self):

        from applications.company.models import Afp

        list_afp = [
            {
                "afp_name": "Capital",
                "afp_code_previred": "401",
                "afp_dependent_worker_rate": 11.44,
                "afp_sis": 1.49,
                "afp_self_employed_worker_rate": 12.93
            },{
                "afp_name": "Cuprum",
                "afp_code_previred": "402",
                "afp_dependent_worker_rate": 11.44,
                "afp_sis": 1.49,
                "afp_self_employed_worker_rate": 12.93
            },{
                "afp_name": "Habitat",
                "afp_code_previred": "403",
                "afp_dependent_worker_rate": 11.27,
                "afp_sis": 1.49,
                "afp_self_employed_worker_rate": 11.76
            },{
                "afp_name": "PlanVital",
                "afp_code_previred": "405",
                "afp_dependent_worker_rate": 11.16,
                "afp_sis": 1.49,
                "afp_self_employed_worker_rate": 11.65
            },{
                "afp_name": "ProVida",
                "afp_code_previred": "406",
                "afp_dependent_worker_rate": 11.5,
                "afp_sis": 1.49,
                "afp_self_employed_worker_rate": 11.94
            },{
                "afp_name": "Modelo",
                "afp_code_previred": "404",
                "afp_dependent_worker_rate": 10.58,
                "afp_sis": 1.49,
                "afp_self_employed_worker_rate": 12.07
            },{
                "afp_name": "Uno",
                "afp_code_previred": "407",
                "afp_dependent_worker_rate": 10.49,
                "afp_sis": 1.49,
                "afp_self_employed_worker_rate": 11.98
            },
        ]

        for afp_data in list_afp:

            # Verificar si el registro ya existe
            if not Afp.objects.using(self.cus_name_bd).filter(afp_code_previred=afp_data['afp_code_previred']).exists():
                Afp.objects.using(self.cus_name_bd).create(
                    **afp_data
                )
    # https://www.spensiones.cl/portal/compendio/596/w3-propertyvalue-4432.html
    populate_customer_base_regions_and_comunnes = property(__populate_customer_base_regions_and_comunnes)
    create_name_db = property(__create_name_db)
    create_data_base = property(__create_database)
    create_migrate_init = property(__create_migrate)
    create_boxes_compensation = property(__create_boxes_compensation)
    create_banks = property(__create_banks)
    create_afp = property(__create_afp)

    def save(self, *args, **kwargs):
        self.cus_name = self.cus_name.lower()
        self.cus_identifier = self.cus_identifier.lower()
        self.cus_name_bd = self.create_name_db

        self.create_data_base
        self.create_migrate_init
        self.populate_customer_base_country
        self.populate_customer_base_regions_and_comunnes
        self.create_boxes_compensation
        self.create_banks
        self.create_afp

        super(Customers, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Listado de Clientes"
        db_table = "customers"
        ordering = ['cus_id']
