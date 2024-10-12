from rest_framework import viewsets

from station.models import Route, Station, Train, CrewMember, Trip
from station.serializers import (
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer, StationSerializer, TrainSerializer, TrainListSerializer, TrainDetailSerializer,
    CrewMemberSerializer, TripSerializer, TripListSerializer, TripDetailSerializer,
)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        if self.action == "retrieve":
            return TrainDetailSerializer
        return TrainSerializer


class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        if self.action == "retrieve":
            return TripDetailSerializer
        return TripSerializer
