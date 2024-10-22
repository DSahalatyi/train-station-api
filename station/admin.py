from django.contrib import admin
from django.contrib.admin import ModelAdmin

from station.models import Station, Route, TrainType, Train, Trip, CrewMember


@admin.register(Station)
class StationAdmin(ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(ModelAdmin):
    pass


@admin.register(TrainType)
class TrainTypeAdmin(ModelAdmin):
    pass


@admin.register(Train)
class TrainAdmin(ModelAdmin):
    pass


@admin.register(CrewMember)
class CrewMemberAdmin(ModelAdmin):
    pass


@admin.register(Trip)
class TripAdmin(ModelAdmin):
    pass
