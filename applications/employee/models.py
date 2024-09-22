from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from applications.company.models import Afp, Bank, Company, GeneralTable, Health, Position, Subsidiary
from applications.humanresources.models import ContractType
from applications.security.models import Commune, Country, Region
from remunerations.choices import (
    CONTRACT_TYPE
    , CONTRIBUTION_TYPE
    , ESTATE_JOB
    , FAMILY_ALLOWANCE_SECTION
    , NOTIFICATION
    , SHAPE
    , TAX_REGIME
    , TYPE_GRATIFICATION
    , WORKER_SECTOR
    , WORKER_TYPE
    , YES_NO_OPTIONS
    , SEX_OPTIONS
    , CIVIL_STATUS_OPTIONS
    , PAYMENT_METHOD_OPTIONS
    , BANK_ACCOUNT_TYPE_OPTIONS
    , STUDY_TYPE_OPTIONS
    , STUDY_STATUS_OPTIONS
)

class UserTypeContract(TimeStampedModel):

    utc_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             db_column="utc_user_id", on_delete=models.PROTECT)
    contractType = models.ForeignKey(
        ContractType, verbose_name="ContractType", db_column="utc_contract_type_id", on_delete=models.PROTECT)
    utc_maincontract = models.CharField(
        "Contrato principal", choices=YES_NO_OPTIONS, max_length=1, default='Y')
    utc_signedcontract = models.CharField(
        "Contrato firmado", choices=YES_NO_OPTIONS, max_length=1, default='Y')
    utc_signedcontractdate = models.DateField("Fecha de contrato firmado", null=True, blank=True)

    def __int__(self):
        return self.utc_id

    def save(self, *args, **kwargs):
        super(UserTypeContract, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_UserTypeContract"
        ordering = ['utc_id']


class Employee(models.Model):
    
    emp_id = models.AutoField("ID", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.PROTECT, null=True, blank=True)
    emp_foreign = models.CharField("Extranjero", choices=YES_NO_OPTIONS, max_length=1, default="Y")
    emp_nationality = models.CharField("Nacionalidad", max_length=100, blank=True, null=True, default='chilen@')
    emp_rut = models.CharField("RUT", max_length=12, unique=True)
    emp_sex = models.CharField("Sexo", max_length=1, choices=SEX_OPTIONS)
    emp_birthdate = models.DateField("Fecha de nacimiento")
    emp_civilstatus = models.IntegerField("Estado civil", choices=CIVIL_STATUS_OPTIONS)
    emp_address = models.TextField("Dirección")
    
    country = models.ForeignKey(Country, verbose_name="Country", db_column="emp_country_id", on_delete=models.PROTECT)
    region = models.ForeignKey(Region, verbose_name="Region", db_column="emp_region_id", on_delete=models.PROTECT)
    commune = models.ForeignKey(Commune, verbose_name="Commune", db_column="empom_commune_id", on_delete=models.PROTECT)
    
    emp_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    emp_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)
    
    emp_studies = models.IntegerField("Tipo de estudios", choices=STUDY_TYPE_OPTIONS, default=1)
    emp_studiesstatus = models.IntegerField("Estado de estudios", choices=STUDY_STATUS_OPTIONS, default=1)
    emp_title = models.CharField("Título", max_length=100, null=True, blank=True)
    
    emp_paymentformat = models.IntegerField("Forma de pago", choices=PAYMENT_METHOD_OPTIONS, null=True, blank=True)
    bank = models.ForeignKey(Bank, verbose_name="Bank", db_column="emp_ban_id", on_delete=models.PROTECT, null=True, blank=True)
    emp_accounttype = models.IntegerField("Tipo de cuenta bancaria", choices=BANK_ACCOUNT_TYPE_OPTIONS, null=True, blank=True)
    emp_bankaccount = models.CharField("Cuenta bancaria", max_length=50, null=True, blank=True)

    emp_drivellicense = models.CharField("Licencia de conducir", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True)
    emp_typelicense = models.CharField("Tipo de lLicencia", max_length=2, null=True, blank=True)
    emp_active = models.CharField("Empleado Activo", choices=YES_NO_OPTIONS, max_length=1, default="Y")

    def __str__(self):
        return f"{self.emp_rut} - {self.user}"
    
    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)

    class Meta:
        db_table = "emp_Employee"
        ordering = ['emp_id']


class UserCompany(TimeStampedModel):

    uc_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="User",
                            db_column="uc_user_id", on_delete=models.PROTECT)
    company = models.ForeignKey(
        Company, verbose_name="Company", db_column="uc_company_id", on_delete=models.PROTECT)
    position = models.ForeignKey(
        Position, verbose_name="Position", db_column="uc_position_id", on_delete=models.PROTECT, null=True, blank=True, related_name="user_emp_position")
    subsidiary = models.ForeignKey(
        Subsidiary, verbose_name="Subsidiary", db_column="uc_subsidiary_id", on_delete=models.PROTECT, null=True, blank=True)
    
    uc_is_boss = models.CharField(
        "Es jefatura", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True, default="N")

    uc_estate_employee = models.IntegerField(
        "Estado de trabajador", choices=ESTATE_JOB, null=True, blank=True)
    uc_workertype = models.IntegerField(
        "Tipo de trabajador", choices=WORKER_TYPE, null=True, blank=True)
    uc_contracttype = models.CharField(
        "Tipo de contrato", choices=CONTRACT_TYPE, max_length=5, null=True, blank=True, default=None)
    uc_hiring_date = models.DateField(
        "Fecha de contratacion del usuario", null=True, blank=True)
    uc_daterenewalcontract = models.DateField(
        "Fecha primer contrato", null=True, blank=True)
    uc_weeklyhours = models.IntegerField(
        "Horas trabajadas", null=True, blank=True, default=45)
    uc_agreedworkdays = models.CharField(
        "Dias de trabajo pactados", null=True, blank=True, max_length=255)
    uc_familyassignment = models.CharField(
        "Asignación familiar", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True, default="N")
    
    uc_family_allowance_section = models.IntegerField(
        "Tramo asignación familiar", choices=FAMILY_ALLOWANCE_SECTION, null=True, blank=True)
    uc_familialloads = models.IntegerField(
        "Cargas familiares", null=True, blank=True, default=0)
    uc_amountfamilyassignment = models.DecimalField(
        "Monto asignación familiar", max_digits=15, decimal_places=2, null=True, blank=True, default=0)
    uc_basesalary = models.DecimalField(
        "Sueldo base", max_digits=15, decimal_places=6, null=True, blank=True, default=0)
    uc_gratification = models.CharField(
        "Tiene gratificación", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True)
    uc_typegratification = models.CharField(
        "Tipo de gratificación", choices=TYPE_GRATIFICATION, max_length=1, null=True, blank=True)
    uc_semanacorrida = models.CharField(
        "Tiene semana corrida", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True)
    uc_workersector = models.IntegerField(
        "Sector del trabajador", choices=WORKER_SECTOR, null=True, blank=True)
    
    afp = models.ForeignKey(Afp, verbose_name="AFP", db_column="uc_afp_id",
                            on_delete=models.PROTECT, null=True, blank=True)
    health = models.ForeignKey(Health, verbose_name="Salud", db_column="uc_health_id",
                                on_delete=models.PROTECT, null=True, blank=True)
    uc_ufisapre = models.FloatField(
        "Valor en UF isapre", null=True, blank=True, default=0)
    uc_funisapre = models.CharField(
        "Fun isapre", max_length=100, null=True, blank=True)

    uc_datenotificationletternotice = models.DateField(
        "Fecha de notificacion carta aviso", null=True, blank=True)
    eu_enddate = models.DateField(
        "Fecha de termino relacion laboral", null=True, blank=True, default=None)
    uc_causal = models.ForeignKey(GeneralTable, verbose_name="GeneralTable",
                                db_column="uc_causal", on_delete=models.PROTECT, null=True, blank=True)
    uc_foundation = models.TextField("Fundamento", null=True, blank=True)
    uc_tiponotication = models.CharField(
        "Tipo de notificacion", choices=NOTIFICATION, max_length=1, null=True, blank=True)
    

    def __int__(self):
        return self.uc_id

    def __str__(self):
        return f"{self.uc_id} - {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        super(UserCompany, self).save(*args, **kwargs)

    class Meta:
        db_table = 'emp_UserCompany'
        ordering = ['uc_id']

