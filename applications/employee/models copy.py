from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from applications.company.models import Bank
from applications.humanresources.models import ContractType
from applications.security.models import Commune, Country, Region
from remunerations.choices import (
    CONTRACT_TYPE, CONTRIBUTION_TYPE, ESTATE_JOB, FAMILY_ALLOWANCE_SECTION, NOTIFICATION, SHAPE, TAX_REGIME, TYPE_GRATIFICATION, WORKER_SECTOR, WORKER_TYPE, YES_NO_OPTIONS, SEX_OPTIONS, CIVIL_STATUS_OPTIONS,
    PAYMENT_METHOD_OPTIONS, BANK_ACCOUNT_TYPE_OPTIONS, 
    STUDY_TYPE_OPTIONS, STUDY_STATUS_OPTIONS
)

class UserTypeContract(TimeStampedModel):
    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )

    utc_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             db_column="utc_user_id", on_delete=models.PROTECT)
    contractType = models.ForeignKey(
        ContractType, verbose_name="ContractType", db_column="utc_contract_type_id", on_delete=models.PROTECT)
    utc_maincontract = models.CharField(
        "Contrato principal", choices=YES_NO_OPTIONS, default='Y')
    utc_signedcontract = models.CharField(
        "Contrato firmado", choices=YES_NO_OPTIONS, default='Y')
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


class UsuarioEmpresa(TimeStampedModel):


    ue_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario",
                            db_column="ue_usuario", on_delete=models.PROTECT)
    empresa = models.ForeignKey(
        Empresa, verbose_name="Empresa", db_column="ue_empresa", on_delete=models.PROTECT)
    cargo = models.ForeignKey(
        Cargo, verbose_name="Cargo", db_column="ue_cargo", on_delete=models.PROTECT, null=True, blank=True, related_name="usuarios_empresa_cargo")
    centrocosto = models.ForeignKey(
        CentroCosto, verbose_name="CentroDecosto ", db_column="ue_contro_costo", on_delete=models.PROTECT, null=True, blank=True)
    sucursal = models.ForeignKey(
        Sucursal, verbose_name="Sucursal", db_column="ue_sucursal", on_delete=models.PROTECT, null=True, blank=True)

    # DATOS LABORALES
    ue_estate = models.IntegerField(
        "Estado de trabajador", choices=ESTATE_JOB, null=True, blank=True)
    ue_tipotrabajdor = models.IntegerField(
        "Tipo de trabajador", choices=WORKER_TYPE, null=True, blank=True)
    ue_tipocontrato = models.CharField(
        "Tipo de contrato", choices=CONTRACT_TYPE, max_length=5, null=True, blank=True, default=None)
    ue_fechacontratacion = models.DateField(
        "Fecha de contratacion del usuario", null=True, blank=True)
    ue_fecharenovacioncontrato = models.DateField(
        "Fecha primer contrato", null=True, blank=True)
    ue_horassemanales = models.IntegerField(
        "Horas trabajadas", null=True, blank=True, default=45)
    ue_agreedworkdays = models.CharField(
        "Dias de trabajo pactados", null=True, blank=True, max_length=255)
    ue_asignacionfamiliar = models.CharField(
        "Asignación familiar", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True, default="N")
    
    ue_family_allowance_section = models.IntegerField(
        "Asignación familiar", choices=FAMILY_ALLOWANCE_SECTION, null=True, blank=True)
    ue_cargasfamiliares = models.IntegerField(
        "Cargas familiares", null=True, blank=True, default=0)
    ue_montoasignacionfamiliar = models.DecimalField(
        "Monto asignación familiar", max_digits=15, decimal_places=2, null=True, blank=True, default=0)
    ue_sueldobase = models.DecimalField(
        "Sueldo base", max_digits=15, decimal_places=6, null=True, blank=True, default=0)
    ue_gratificacion = models.CharField(
        "Tiene gratificación", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True)
    ue_tipogratificacion = models.CharField(
        "Tipo de gratificación", choices=TYPE_GRATIFICATION, max_length=1, null=True, blank=True)
    ue_comiciones = models.CharField(
        "Tiene comociones", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True)
    ue_porcentajecomicion = models.DecimalField(
        "Porcentaje comociones", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_semanacorrida = models.CharField(
        "Tiene semana corrida", choices=YES_NO_OPTIONS, max_length=1, null=True, blank=True)
    
    ue_workersector = models.IntegerField(
        "Sector del trabajador", choices=WORKER_SECTOR, null=True, blank=True)
    
    # AFP
    afp = models.ForeignKey(Afp, verbose_name="AFP", db_column="ue_afp",
                            on_delete=models.PROTECT, null=True, blank=True)

    # Caja Compensacion
    caja_compensacion = models.ForeignKey(CajasCompensacion, verbose_name="CajasCompensacion",
                                          db_column="ue_caja_compensacion", on_delete=models.PROTECT, null=True, blank=True)

    # APV
    ue_tieneapv = models.CharField(
        "Tiene APV", choices=YES_NO_OPTIONS, max_length=1, default="N", null=True, blank=True)
    apv = models.ForeignKey(Apv, verbose_name="APV", db_column="us_apv",
                            on_delete=models.PROTECT, null=True, blank=True)
    ue_contributiontype = models.IntegerField(
        "Tipo de contribución", choices=CONTRIBUTION_TYPE, null=True, blank=True)
    ue_taxregime = models.IntegerField(
        "Régimen tributario", choices=TAX_REGIME, null=True, blank=True)
    ue_shape = models.IntegerField(
        "Forma del aporte", choices=SHAPE, null=True, blank=True)
    ue_apvamount = models.DecimalField(
        "Monto", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_paymentperioddate = models.DateField(
        "Fecha periodo de pago", null=True, blank=True)

    # COTIZACIONES VOLUNTARIAS
    ue_tieneahorrovoluntario = models.CharField(
        "Tiene ahorro voluntario", choices=YES_NO_OPTIONS, max_length=1, default="N", null=True, blank=True)
    ue_cotizacionvoluntaria = models.DecimalField(
        "Cotización voluntaria", max_digits=15, decimal_places=2, null=True, blank=True)
    ue_ahorrovoluntario = models.DecimalField(
        "Ahorro Voluntario", max_digits=15, decimal_places=2, null=True, blank=True)

    # SALUD
    salud = models.ForeignKey(Salud, verbose_name="Salud", db_column="ue_salud",
                              on_delete=models.PROTECT, null=True, blank=True)
    ue_ufisapre = models.FloatField(
        "Valor en UF isapre", null=True, blank=True, default=0)
    ue_funisapre = models.CharField(
        "Fun isapre", max_length=100, null=True, blank=True)
    ue_cotizacion = models.FloatField(
        "Cotizacion fonasa/isapre", null=True, blank=True, default=0)

    # SEGURO DE DESEMPLEO
    ue_segurodesempleo = models.CharField(
        "Seguro de desmpleo", max_length=1, choices=YES_NO_OPTIONS, null=True, blank=True)
    ue_porempleado = models.FloatField(
        "porcentaje por empleado", null=True, blank=True, default=0)
    ue_porempleador = models.FloatField(
        "porcentaje por empleador", null=True, blank=True, default=0)
    ue_trabajopesado = models.CharField(
        "Trabajo pesado", choices=YES_NO_OPTIONS, max_length=1, default="N", null=True, blank=True)

    # ENTREGA DE EQUIPOS SEGURIDAD Y OTROS
    ue_entregaequiposeguridad = models.CharField(
        "Entrega equipos de seguridad y otros", max_length=1, choices=YES_NO_OPTIONS, null=True, blank=True)
    ue_descripcionentrega = models.TextField(
        "Descpricion de la entrega de equipos y seguridad", default="N", null=True, blank=True)

    # TERMINO RELACION LABORAL
    ue_fechanotificacioncartaaviso = models.DateField(
        "Fecha de notificacion carta aviso", null=True, blank=True)
    ue_fechatermino = models.DateField(
        "Fecha de termino relacion laboral", null=True, blank=True, default=None)
    ue_cuasal = models.ForeignKey(TablaGeneral, verbose_name="TablaGeneral",
                                db_column="ue_causal", on_delete=models.PROTECT, null=True, blank=True)
    ue_fundamento = models.TextField("Fundamento", null=True, blank=True)
    ue_tiponoticacion = models.CharField(
        "Tipo de notificacion", choices=NOTIFICATION, max_length=1, null=True, blank=True)

    def __int__(self):
        return self.ue_id

    def __str__(self):
        return f"{self.ue_id} - {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        # print "save cto"
        super(UsuarioEmpresa, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_usuario_empresa'
        ordering = ['ue_id']

class Contact(TimeStampedModel):
    TYPE = (
        (1, 'Email Personal'),
        (2, 'Email Corporativo'),
        (3, 'Teléfono Movil'),
        (4, 'Teléfono Fijo'),
        (5, 'Teléfono Familiar'),
        (6, 'Email Familiar'),
    )

    OPCIONES = (
        ('S', 'SI'),
        ('N', 'NO'),
    )

    con_id = models.AutoField("Key", primary_key=True)
    con_contact_type = models.IntegerField(
        "Tipo de contacto", choices=TYPE, default=2)
    con_mail_contact = models.CharField(
        "Correo de contacto", max_length=120, null=True, blank=True)
    con_phone_contact = models.CharField(
        "Teléfono de contacto", max_length=120, null=True, blank=True)
    cont_name_contact = models.CharField("Nombre del contacto", max_length=150)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             db_column="con_user", on_delete=models.PROTECT)
    con_actiove = models.CharField(
        "Contacto activo", choices=OPCIONES, max_length=1, default="S")

    def __int__(self):
        return self.con_id

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_contact'
        ordering = ['con_id']


class ConceptUser(TimeStampedModel):

    REMUNERATION_TYPE = (
        (1, 'Orinarias'),
        (2, 'Extraordinarias'),
        (3, 'Especiales'),
    )

    cu_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Usuario",
                             db_column="cu_usuario_id", on_delete=models.PROTECT)
    concept = models.ForeignKey(
        Concept, verbose_name="Concept", db_column="cu_concept_id", on_delete=models.PROTECT)
    cu_typeremuneration = models.IntegerField("Fórmula", choices=REMUNERATION_TYPE, null=True, blank=True)
    cu_formula = models.FloatField("Fórmula", null=True, blank=True)
    cu_value = models.FloatField("Valor", null=True, blank=True, default=0)
    cu_search_field = models.CharField("Campo de busqueda", null=True, blank=True, default=0, max_length=50)
    cu_description = models.CharField(
        "Descripción", max_length=150, null=True, blank=True)

    def __int__(self):
        return self.cu_id

    def __str__(self):
        return f"{self.cu_id} - {self.user.username} - {self.concept.conc_id}"

    def save(self, *args, **kwargs):
        super(ConceptUser, self).save(*args, **kwargs)

    class Meta:
        db_table = 'usu_concept_user'
        ordering = ['cu_id']


class FamilyResponsibilities(TimeStampedModel):

    SEXO = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
    )

    RELATIONSSHIP = (
        (0, '---------'),
        (1, 'Padre/Madre'),
        (2, 'Hij@'),
        (3, 'Herman@'),
        (4, 'Cónyuge'),
    )

    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )
    
    fr_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Colaborador",
                             db_column="fr_user", null=True, blank=True, on_delete=models.PROTECT)
    fr_rut = models.CharField("Rut", max_length=100)
    fr_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    fr_relationship = models.IntegerField("Parentezco", choices=RELATIONSSHIP)
    fr_firstname = models.CharField("Nombres", max_length=150)
    fr_lastname = models.CharField("Apellidos", max_length=150)
    fr_fechanacimiento = models.DateField("Fecha de nacimiento")
    fr_activo = models.IntegerField(
        "Activo", choices=OPCIONES, default=1)

    def __int__(self):
        return self.col_id
    
    def __str__(self):
        return f"{self.fr_id} - {self.user.first_name} {self.user.last_name} - {self.fr_firstname} {self.fr_lastname}"

    def save(self, *args, **kwargs):
        super(FamilyResponsibilities, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_family_responsibilities"
        ordering = ['fr_id']