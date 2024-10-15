from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import Ticket, Order
from station.serializers import TripTicketSerializer, TripDetailSerializer


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "car",
            "place",
            "trip",
        )

    def validate(self, attrs):
        Ticket.validate_place_car(
            car=attrs["car"],
            place=attrs["place"],
            trip=attrs["trip"],
            error_to_raise=ValidationError,
        )
        return super().validate(attrs)


class TicketListSerializer(TicketSerializer):
    trip = TripTicketSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket in tickets_data:
                Ticket.objects.create(order=order, **ticket)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
