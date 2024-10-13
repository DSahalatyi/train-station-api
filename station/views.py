from rest_framework import viewsets

from station.models import Route, Station, Train, CrewMember, Trip
from station.serializers import (
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    StationSerializer,
    TrainSerializer,
    TrainListSerializer,
    TrainDetailSerializer,
    CrewMemberSerializer,
    TripSerializer,
    TripListSerializer,
    TripDetailSerializer,
)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("source", "destination")

        return queryset

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = RouteListSerializer
        if self.action == "retrieve":
            serializer = RouteDetailSerializer

        return serializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("train_type")

        return queryset

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = TrainListSerializer
        if self.action == "retrieve":
            serializer = TrainDetailSerializer

        return serializer


class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related(
                "route__source",
                "route__destination",
                "train",
            ).prefetch_related("crew")

        return queryset

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = TripListSerializer
        if self.action == "retrieve":
            serializer = TripDetailSerializer

        return serializer
