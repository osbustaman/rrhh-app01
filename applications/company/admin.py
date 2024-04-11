from django.contrib import admin

from applications.company.models import BoxesCompensation, MutualSecurity, Company, Subsidiary

# Register your models here.
class SubsidiaryAdmin(admin.ModelAdmin):
    list_display = ['sub_id', 'sub_name', 'company', 'sub_active']
    list_filter = ['sub_name', 'sub_active', 'company']
    search_fields = ['sub_name', 'company']
    list_per_page = 10


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['com_id', 'com_rut', 'com_name_company', 'com_social_reason', 'com_twist_company', 'com_active']
    list_filter = ['com_rut', 'com_name_company']
    search_fields = ['com_rut', 'com_name_company']
    list_per_page = 10


class MutualSecurityAdmin(admin.ModelAdmin):
    list_display = ['ms_id', 'ms_name', 'ms_rut', 'ms_codeprevired', 'ms_active']
    list_filter = ['ms_name', 'ms_rut']
    search_fields = ['ms_name', 'ms_rut']
    list_per_page = 10


class BoxesCompensationAdmin(admin.ModelAdmin):
    list_display = ['bc_id', 'bc_rut', 'bc_business_name', 'bc_fantasy_name', 'bc_phone', 'bc_email', 'bc_address']
    list_filter = ['bc_fantasy_name', 'country__cou_name', 'region__re_name', 'commune__com_name']
    search_fields = ['bc_rut', 'bc_fantasy_name', 'bc_business_name']
    list_per_page = 10


admin.site.register(Subsidiary, SubsidiaryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(MutualSecurity, MutualSecurityAdmin)
admin.site.register(BoxesCompensation, BoxesCompensationAdmin)