from django.contrib import admin

# Register your models here.
from configuration_side.models import Command

admin.site.register(Command)