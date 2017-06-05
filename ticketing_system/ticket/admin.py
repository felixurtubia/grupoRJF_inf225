from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Empleado

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmpleadoInline(admin.StackedInline):
    model = Empleado
    can_delete = False
    verbose_name_plural = 'empleados'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmpleadoInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
