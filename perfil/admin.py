from django.contrib import admin

# Register your models here.
from .models import Categoria, Conta


admin.site.register(Categoria)
admin.site.register(Conta)