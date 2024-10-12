from django.urls import include, path
from rest_framework import routers

from order.views import OrderViewSet
from station.views import RouteViewSet, StationViewSet, TrainViewSet, CrewMemberViewSet, TripViewSet

app_name = "station"

router = routers.DefaultRouter()

router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("trains", TrainViewSet)
router.register("crew-members", CrewMemberViewSet)
router.register("trips", TripViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]