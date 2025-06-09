from django.db.models import F, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from station.filters import TripFilter
from station.models import Route, Station, Train, CrewMember, Trip
from station.pagination import TripPagination
from station.schemas.crew_members import crew_members_viewset_schema
from station.schemas.routes import routes_viewset_schema
from station.schemas.stations import stations_viewset_schema
from station.schemas.trains import trains_viewset_schema
from station.schemas.trips import trips_viewset_schema
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
    CrewMemberListSerializer,
    CrewMemberImageSerializer,
    CrewMemberDetailSerializer,
)


@stations_viewset_schema
class StationViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@routes_viewset_schema
class RouteViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

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


@trains_viewset_schema
class TrainViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

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


@crew_members_viewset_schema
class CrewMemberViewSet(viewsets.ModelViewSet):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = CrewMemberListSerializer

        if self.action == "retrieve":
            serializer = CrewMemberDetailSerializer

        if self.action == "upload_image":
            serializer = CrewMemberImageSerializer

        return serializer

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        crew_member = self.get_object()
        serializer = self.get_serializer(crew_member, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@trips_viewset_schema
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    pagination_class = TripPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TripFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related().prefetch_related("crew").distinct()

        if self.action == "list":
            queryset = queryset.annotate(
                places_available=F("train__car_num") * F("train__places_in_car")
                - Count("tickets")
            )

        return queryset

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = TripListSerializer
        if self.action == "retrieve":
            serializer = TripDetailSerializer

        return serializer
