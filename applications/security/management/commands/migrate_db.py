from django import conf
from django.core.management.base import BaseCommand
from decouple import config
from django.core.management import call_command
from applications.security.models import Customers

class Command(BaseCommand):
    help = 'Se inicia la migracion para todas las bases de datos'

    def handle(self, *args, **options):

        list_objects_bd = Customers.objects.all()

        for bd in list_objects_bd:

            the_bd = {}
            the_bd['ENGINE'] = config('ENGINE')
            the_bd['HOST'] = config('HOST')
            the_bd['NAME'] = bd.cus_name_bd
            the_bd['USER'] = config('USER')
            the_bd['PASSWORD'] = config('PASSWORD')
            the_bd['PORT'] = config('PORT')

            conf.settings.DATABASES[bd.cus_name_bd] = the_bd
            call_command('migrate', database=bd.cus_name_bd)

        self.stdout.write('¡La migracion para todas las bases de datos fue realizada con exito!')