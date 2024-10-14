from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from order.models import Order, Ticket
from station.models import Station, TrainType, Train, Route, Trip


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@email.com", password="testpass123"
        )

    def test_order_str(self):
        order = Order.objects.create(
            user=self.user,
        )
        self.assertEqual(str(order), f"{self.user} | {order.created_at}")


class TicketModelTests(TestCase):
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

    def test_ticket_str(self):
        ticket = Ticket.objects.create(car=1, place=1, trip=self.trip, order=self.order)
        self.assertEqual(
            str(ticket), f"{ticket.trip} - (car - {ticket.car}, place - {ticket.place})"
        )

    def test_ticket_invalid_place(self):
        with self.assertRaises(ValidationError) as context:
            Ticket.objects.create(car=1, place=11, trip=self.trip, order=self.order)
        self.assertEqual(
            str(context.exception),
            f"{{'place': ['place number must be in available range: "
            f"(1, places_in_car): (1, {self.train.places_in_car})']}}",
        )
        self.assertEqual(Ticket.objects.count(), 0)

    def test_ticket_invalid_car(self):
        with self.assertRaises(ValidationError) as context:
            Ticket.objects.create(car=2, place=1, trip=self.trip, order=self.order)
        self.assertEqual(
            str(context.exception),
            f"{{'car': ['car number must be in available range: "
            f"(1, car_num): (1, {self.train.car_num})']}}",
        )
        self.assertEqual(Ticket.objects.count(), 0)