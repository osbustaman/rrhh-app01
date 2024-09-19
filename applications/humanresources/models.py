from django.db import models
from model_utils.models import TimeStampedModel

from applications.company.models import Company
from remunerations.choices import CLASSIFICATION, REMUNERATION_TYPE, SEARCH_FIELDS, TYPE_CLASSIFICATION, TYPE_VARIABLE, YES_NO_OPTIONS

# Create your models here.

class ContractType(TimeStampedModel):
    ct_id = models.AutoField("Key", primary_key=True)
    ct_contractcode = models.CharField("Código contrato", max_length=25)
    ct_contractname = models.CharField("Nombre contrato", max_length=100)
    company = models.ForeignKey(Company, verbose_name="Company",
                                db_column="ct_company_id", on_delete=models.PROTECT)
    ct_contract = models.TextField("Texto del contrato")
    ct_active = models.CharField(
        "activo", choices=YES_NO_OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.ct_id

    def __str__(self):
        return f'{self.ct_contractname}'

    def save(self, *args, **kwargs):
        super(ContractType, self).save(*args, **kwargs)

    class Meta:
        db_table = "hr_ContractType"
        ordering = ['ct_id']


class MonthlyPreviredData(TimeStampedModel):

    dpm_id = models.AutoField("Key", primary_key=True)
    dpm_name = models.CharField("Nombre", max_length=255)
    dpm_shot_name = models.CharField("Nombre Corto", max_length=50, null=True, blank=True)
    dpm_month = models.IntegerField("mes")
    dpm_year = models.IntegerField("año")
    dpm_day = models.IntegerField("dia")
    dpm_dict = models.TextField("Diccionario de remuneraciones mensuales", null=True, blank=True)
    dpm_active = models.CharField(
        "activo", choices=YES_NO_OPTIONS, max_length=1, default="Y")
    
    def __int__(self):
        return self.dpm_id

    def __str__(self):
        return f"{self.dpm_id} - {self.dpm_name}"

    def save(self, *args, **kwargs):
        super(MonthlyPreviredData, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hr_MonthlyPreviredData'
        ordering = ['dpm_id']


class Concept(TimeStampedModel):

    conc_id = models.AutoField("Key", primary_key=True)
    conc_name = models.CharField("Nombre", max_length=255)
    conc_clasificationconcept = models.IntegerField("Clasificación concepto", choices=CLASSIFICATION)
    conc_typeconcept = models.IntegerField("Tipo concepto", choices=TYPE_CLASSIFICATION)
    conc_remuneration_type = models.IntegerField("Tipo de remuneración", choices=REMUNERATION_TYPE)
    conc_search_field = models.CharField("Campo de busqueda", null=True, blank=True, default='0', max_length=50, choices=SEARCH_FIELDS)
    conc_default = models.CharField(
        "Concepto por defecto", choices=YES_NO_OPTIONS, max_length=1, default="N")
    conc_active = models.CharField(
        "Concepto activo", choices=YES_NO_OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.conc_id

    def __str__(self):
        return f"{self.conc_id} - {self.conc_name}"

    def save(self, *args, **kwargs):
        super(Concept, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hr_Concept'
        ordering = ['conc_id']


class ConfigVariableRemunerations(TimeStampedModel):
    
    cvr_id = models.AutoField("Key", primary_key=True)
    cvr_name = models.CharField("Nombre variable", max_length=255)
    cvr_valueone = models.CharField("Valor uno", max_length=255, null=True, blank=True)
    cvr_valuetwo = models.CharField("Valor dos", max_length=255, null=True, blank=True)

    cvr_vartype = models.IntegerField(
        "Tipo de variable", choices=TYPE_VARIABLE, default=0)

    cvr_active = models.CharField(
        "Variable activa", choices=YES_NO_OPTIONS, max_length=1, default="Y")

    def __int__(self):
        return self.cvr_id

    def __str__(self):
        return f"{self.cvr_id} - {self.cvr_name}"

    def save(self, *args, **kwargs):
        super(ConfigVariableRemunerations, self).save(*args, **kwargs)

    class Meta:
        db_table = 'hr_ConfigVariableRemunerations'
        ordering = ['cvr_id']