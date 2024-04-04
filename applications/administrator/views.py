from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from applications.administrator.forms import AdminUserForm
from applications.security.models import Customers

# Create your views here.


@login_required
def add_admin(request, client_id):

    lista_err = []
    object_client = Customers.objects.get(cus_name_bd=request.POST["database_name"])
    form = AdminUserForm(request.POST)
    if form.is_valid():
        admin_user = form.save(commit=False)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password(request.POST['password'])
        admin_user.save(using=object_client.cus_name_bd)

        messages.success(request, 'Usuario creado con éxito')
    else:
        for field in form:
            for error in field.errors:
                lista_err.append(field.label + ': ' + error)

        messages.error(request, lista_err)

    return redirect(reverse('admin:security_customer_changelist'))  # Redireccionar al listado de objetos del modelo