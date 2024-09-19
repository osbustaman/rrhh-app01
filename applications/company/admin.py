from django.contrib import admin

from applications.company.models import Area, BoxesCompensation, Department, MutualSecurity, Company, Position, Subsidiary

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

class AreaAdmin(admin.ModelAdmin):
    list_display = ['ar_id', 'ar_name', 'company', 'ar_active']
    list_filter = ['ar_name', 'company__com_name_company']
    search_fields = ['ar_name']
    list_per_page = 10


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dep_id', 'dep_name', 'area', 'dep_active']
    list_filter = ['dep_name']
    search_fields = ['dep_name']
    list_per_page = 10


class PositionAdmin(admin.ModelAdmin):
    list_display = ['pos_id', 'pos_name_position', 'departament', 'pos_active']
    list_filter = ['pos_name_position']
    search_fields = ['pos_name_position']
    list_per_page = 10

admin.site.register(Subsidiary, SubsidiaryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(MutualSecurity, MutualSecurityAdmin)
admin.site.register(BoxesCompensation, BoxesCompensationAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position, PositionAdmin)