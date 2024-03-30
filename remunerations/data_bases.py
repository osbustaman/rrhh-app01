import django.conf as conf
from decouple import config

from applications.security.models import Customers

def load_data_base():

    customers_list = Customers.objects.using('default').all()

    for base in customers_list:

        domain = base.cus_name_bd
        
        nueva_base = {}
        nueva_base['ENGINE'] = config('ENGINE')
        nueva_base['HOST'] = config('HOST')
        nueva_base['NAME'] = base.cus_name_bd
        nueva_base['USER'] = config('USER')
        nueva_base['PASSWORD'] = config('PASSWORD')
        nueva_base['PORT'] = config('PORT')

        conf.settings.DATABASES[domain] = nueva_base