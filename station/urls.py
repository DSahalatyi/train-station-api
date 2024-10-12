from django.urls import include, path
from rest_framework import routers

from station.views import RouteViewSet, StationViewSet, TrainViewSet, CrewMemberViewSet, TripViewSet

app_name = "station"

router = routers.DefaultRouter()

router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("trains", TrainViewSet)
router.register("crew-members", CrewMemberViewSet)
router.register("trips", TripViewSet)

urlpatterns = [
    path("", include(router.urls)),
]