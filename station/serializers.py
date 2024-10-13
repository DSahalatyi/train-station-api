from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from station.models import Station, Route, TrainType, Train, CrewMember, Trip


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

    def validate(self, attrs):
        Route.validate_source_destination(
            attrs["source"], attrs["destination"], ValidationError
        )
        return super().validate(attrs)


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(read_only=True, slug_field="name")


class RouteDetailSerializer(RouteSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = "__all__"


class TrainListSerializer(TrainSerializer):
    train_type = serializers.SlugRelatedField(read_only=True, slug_field="name")


class TrainDetailSerializer(TrainSerializer):
    train_type = TrainTypeSerializer(read_only=True)


class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = ("id", "first_name", "last_name")


class CrewMemberListSerializer(CrewMemberSerializer):
    class Meta(CrewMemberSerializer.Meta):
        fields = ("id", "full_name")


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"

    def validate(self, attrs):
        departure_time = attrs.get("departure_time")
        arrival_time = attrs.get("arrival_time")
        crew_members = attrs.get("crew", [])
        train = attrs.get("train")

        if departure_time < timezone.now():
            raise ValidationError("Departure time must be in the future")

        if arrival_time < departure_time:
            raise ValidationError("Arrival time must be after the departure time")

        overlapping_trips = Trip.objects.filter(
            Q(departure_time__lt=arrival_time, arrival_time__gt=departure_time)
        ).exclude(id=self.instance.id if self.instance else None)

        for crew_member in crew_members:
            if overlapping_trips.filter(crew=crew_member).exists():
                raise ValidationError(
                    f"Crew member {crew_member} is already assigned to another trip during this time."
                )

        if overlapping_trips.filter(train=train).exists():
            raise ValidationError(
                f"Train {train} is already assigned to another train during this time."
            )

        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get("request")
        if not request.user.is_staff:
            representation.pop("crew", None)

        return representation


class TripListSerializer(TripSerializer):
    route = SerializerMethodField(read_only=True)
    train = SlugRelatedField(read_only=True, slug_field="name")
    crew = SlugRelatedField(many=True, read_only=True, slug_field="full_name")

    def get_route(self, trip):
        return str(trip.route)


class TripTicketSerializer(TripListSerializer):
    class Meta(TripSerializer.Meta):
        fields = (
            "id",
            "route",
            "train",
            "departure_time",
            "arrival_time",
        )


class TripDetailSerializer(TripSerializer):
    route = RouteListSerializer(read_only=True)
    train = TrainListSerializer(read_only=True)
    crew = CrewMemberListSerializer(many=True, read_only=True)
