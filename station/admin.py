from django.contrib import admin
from django.contrib.admin import ModelAdmin

from station.models import Station


@admin.register(Station)
class StationAdmin(ModelAdmin):
    pass