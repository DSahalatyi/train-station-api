from django.contrib import admin
from django.contrib.admin import ModelAdmin

from station.models import Station, Route


@admin.register(Station)
class StationAdmin(ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(ModelAdmin):
    pass