from django.contrib import admin
from .models import RegistroEvento, Usuario, Evento
# Register your models here.
admin.site.register(RegistroEvento)
admin.site.register(Usuario)
admin.site.register(Evento)