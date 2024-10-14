from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from order.models import Order
from order.serializers import TicketSerializer
from station.models import Station, Route, TrainType, Train, Trip


class TicketSerializerTests(TestCase):
    def setUp(self):
        source_station = Station.objects.create(
            name="Source Station", latitude=1, longitude=1
        )
        destination_station = Station.objects.create(
            name="Destination Station", latitude=2, longitude=2
        )
        route = Route.objects.create(
            source=source_station, destination=destination_station, distance=1
        )
        train_type = TrainType.objects.create(name="Test")
        self.train = Train.objects.create(
            name="Test Train", car_num=1, places_in_car=10, train_type=train_type
        )
        self.trip = Trip.objects.create(
            route=route,
            train=self.train,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
        )
        self.user = get_user_model().objects.create_user(
            email="test@email.com", password="testpass123"
        )
        self.order = Order.objects.create(user=self.user)

    def test_ticket_serializer_valid(self):
        data = {"car": 1, "place": 1, "trip": self.trip.id, "order": self.order.id}
        serializer = TicketSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_ticket_serializer_invalid_place(self):
        data = {"car": 1, "place": 11, "trip": self.trip.id, "order": self.order.id}
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["place"][0],
            f"place number must be in available range: (1, places_in_car): (1, {self.train.places_in_car})",
        )

    def test_ticket_serializer_invalid_car(self):
        data = {"car": 2, "place": 1, "trip": self.trip.id, "order": self.order.id}
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["car"][0],
            f"car number must be in available range: (1, car_num): (1, {self.train.car_num})",
        )
