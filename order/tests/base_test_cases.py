from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from order.models import Order
from station.models import Station, Route, TrainType, Train, Trip


class BaseTicketTests(TestCase):
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
