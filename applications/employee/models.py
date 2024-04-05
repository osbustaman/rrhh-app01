from django.db import models

from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from applications.company.models import Bank
from applications.security.models import Commune, Country, Region

# Create your models here.

"""class Colaborador(TimeStampedModel):

    OPCIONES = (
        (1, 'SI'),
        (0, 'NO'),
    )

    SEXO = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
    )

    ESTADO_CIVIL = (
        (1, 'Solter@'),
        (2, 'Casad@'),
        (3, 'Divorsiad@'),
        (4, 'Viud@'),
    )

    TIPO_USUARIO = (
        (1, 'Super-Admin'),
        (2, 'Recursos Humanos'),
        (3, 'Recursos Humanos Administrador'),
        (4, 'Jefatura'),
        (5, 'Colaborador'),
    )

    FORMA_PAGO = (
        ('', '---------'),
        (1, 'Efectivo'),
        (2, 'Cheque'),
        (3, 'Vale vista'),
        (4, 'Depósito directo'),
    )

    TIPO_CUENTA_BANCARIA = (
        (0, '---------'),
        (1, 'CUENTA VISTA'),
        (2, 'CUENTA DE AHORRO'),
        (3, 'CUENTA BANCARIA PARA ESTUDIANTE'),
        (4, 'CUENTA CHEQUERA ELECTRÓNICA'),
        (5, 'CUENTA RUT'),
        (6, 'CUENTA BANCARIA PARA EXTRANJEROS'),
        (7, 'CUENTA CORRIENTE')
    )

    TIPO_ESTUDIOS = (
        (1, 'ENSEÑANZA MEDIA'),
        (2, 'ESTUDIOS SUPERIORES (CFT)'),
        (3, 'ESTUDIOS UNIVERSITARIOS'),
    )

    ESTADO_ESTUDIOS = (
        (1, 'COMPLETO'),
        (2, 'INCOMPLETO'),
    )

    col_id = models.AutoField("Key", primary_key=True)
    user = models.ForeignKey(User, verbose_name="Colaborador",
                             db_column="ue_usuario", null=True, blank=True, on_delete=models.PROTECT)
    col_extranjero = models.IntegerField(
        "Extranjero", choices=OPCIONES, default=0)
    col_nacionalidad = models.CharField(
        "Nacionalidad", max_length=100, blank=True, null=True, default='chilen@')
    col_rut = models.CharField("Rut", max_length=100)
    col_sexo = models.CharField("Sexo", max_length=1, choices=SEXO)
    col_fechanacimiento = models.DateField("Fecha de nacimiento")
    col_estadocivil = models.IntegerField("Estado civil", choices=ESTADO_CIVIL)
    col_direccion = models.TextField("Dirección")
    pais = models.ForeignKey(Country, verbose_name="País",
                             db_column="usu_pais", on_delete=models.PROTECT)
    region = models.ForeignKey(
        Region, verbose_name="Región", db_column="usu_region", on_delete=models.PROTECT)
    comuna = models.ForeignKey(
        Commune, verbose_name="Comuna", db_column="usu_comuna", on_delete=models.PROTECT)
    col_latitude = models.CharField("Latitud", max_length=255, null=True, blank=True)
    col_longitude = models.CharField("Longitud", max_length=255, null=True, blank=True)


    col_estudios = models.IntegerField(
        "Tipo estudios", choices=TIPO_ESTUDIOS, default=1)
    col_estadoestudios = models.IntegerField(
        "Estado estudios", choices=ESTADO_ESTUDIOS, default=1)
    col_titulo = models.CharField(
        "Titulo", max_length=100, null=True, blank=True)
    col_formapago = models.IntegerField(
        "Forma de pago", choices=FORMA_PAGO, null=True, blank=True)
    banco = models.ForeignKey(Bank, verbose_name="Banco", db_column="ue_banco",
                              null=True, blank=True, on_delete=models.PROTECT)
    col_tipocuenta = models.IntegerField(
        "tipo de cuenta", choices=TIPO_CUENTA_BANCARIA, null=True, blank=True)
    col_cuentabancaria = models.CharField(
        "Cuenta bancaria", max_length=50, null=True, blank=True)
    col_usuarioactivo = models.IntegerField(
        "Usuario activo", choices=OPCIONES, default=1)
    col_licenciaconducir = models.IntegerField(
        "Licencia de conducir", choices=OPCIONES, null=True, blank=True)
    col_tipolicencia = models.CharField(
        "Tipo de licencia", max_length=2, null=True, blank=True)
    col_fotousuario = models.TextField("Foto usuario", null=True, blank=True)
    col_activo = models.IntegerField(
        "Colaborador Activo", choices=OPCIONES, default=1)

    def __int__(self):
        return self.col_id
    
    def __str__(self):
        return f"{self.col_id} - {self.col_rut}"

    def save(self, *args, **kwargs):
        super(Colaborador, self).save(*args, **kwargs)

    class Meta:
        db_table = "usu_colaborador"
        ordering = ['col_id']"""