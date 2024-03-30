from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import Customers, ListItems, ListSubItems, Menu, MenuItems


# Register your models here.


class MenuAdmin(admin.ModelAdmin):
    list_display = ['m_id', 'm_user', 'm_name', 'm_active']
    list_filter = ['m_name', 'm_active']
    search_fields = ['m_user']
    list_per_page = 10

class ListItemsAdmin(admin.ModelAdmin):
    list_display = ['li_id', 'li_name', 'li_short_name', 'li_order', 'li_icon', 'li_active']
    list_filter = ['li_name', 'li_active']
    search_fields = ['li_name', 'li_short_name']
    list_per_page = 10

class MenuItemsAdmin(admin.ModelAdmin):
    list_display = ['mi_menu', 'mi_items']
    list_filter = ['mi_menu__m_user__username', 'mi_menu__m_user__email', 'mi_items__li_name']
    search_fields = ['mi_menu__m_user__username', 'mi_menu__m_user__email']
    list_per_page = 10

class ListSubItemsAdmin(admin.ModelAdmin):
    list_display = ['lsi_id', 'lsi_name', 'lsi_order', 'lsi_url', 'lsi_items', 'lsi_active']
    list_filter = ['lsi_name', 'lsi_items__li_name', 'lsi_active']
    search_fields = ['lsi_name', 'lsi_items__li_name']
    list_per_page = 10

class CustomersAdmin(admin.ModelAdmin):
    list_display = ['cus_id', 'cus_name', 'cus_date_in', 'cus_date_out', 'cus_active']
    list_filter = ['cus_name_bd']
    search_fields = ['cus_name', 'cus_name_bd', 'cus_active']
    list_per_page = 10

    change_form_template = "admin/btn_migrate.html"

    def response_change(self, request, obj):
        if "migrate_db" in request.POST:
            self.message_user(request, "La base de datos fue migrada correctamente", "success")
            return HttpResponseRedirect(".")
        
        return super().response_change(request, obj)


admin.site.register(Menu, MenuAdmin)
admin.site.register(ListItems, ListItemsAdmin)
admin.site.register(MenuItems, MenuItemsAdmin)
admin.site.register(ListSubItems, ListSubItemsAdmin)
admin.site.register(Customers, CustomersAdmin)