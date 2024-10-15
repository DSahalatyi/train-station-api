from django.test import TestCase
from django.utils import timezone

from station.models import Station, Route, TrainType, Train, CrewMember, Trip
from station.tests.base_test_cases import BaseTripTests


class StationModelTests(TestCase):
    def test_station_str(self):
        station = Station.objects.create(name="Test Station", latitude=1, longitude=1)
        self.assertEqual(str(station), station.name)


class RouteModelTests(TestCase):
    def setUp(self):
        self.source_station = Station.objects.create(
            name="Source Station", latitude=1, longitude=1
        )
        self.destination_station = Station.objects.create(
            name="Destination Station", latitude=2, longitude=2
        )

    def test_route_str(self):
        route = Route.objects.create(
            source=self.source_station, destination=self.destination_station, distance=1
        )
        self.assertEqual(
            str(route),
            f"{route.source.name} - {route.destination.name} ({str(route.distance)} km)",
        )


class TrainTypeModelTests(TestCase):
    def test_train_type_str(self):
        train_type = TrainType.objects.create(name="Test Train Type")
        self.assertEqual(str(train_type), train_type.name)


class TrainModelTests(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Test Train Type")

    def test_train_str(self):
        train = Train.objects.create(
            name="Test Train", car_num=1, places_in_car=10, train_type=self.train_type
        )
        self.assertEqual(str(train), train.name)


class CrewModelTests(TestCase):
    def test_crew_member_str(self):
        crew_member = CrewMember.objects.create(first_name="Test", last_name="Testing")
        self.assertEqual(str(crew_member), crew_member.full_name)


class TripModelTests(BaseTripTests):
    def test_trip_str(self):
        trip = Trip.objects.create(
            route=self.route,
            train=self.train,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
        )
        self.assertEqual(
            str(trip), f"{trip.departure_time} | {trip.route} | {trip.train}"
        )
