from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from station.models import Station, CrewMember, Trip, Train
from station.serializers import RouteSerializer, TripSerializer
from station.tests.base_test_cases import BaseTripTests


class RouterSerializerTests(TestCase):
    def setUp(self):
        self.source_station = Station.objects.create(
            name="Source Station", latitude=1, longitude=1
        )
        self.destination_station = Station.objects.create(
            name="Destination Station", latitude=2, longitude=2
        )

    def test_route_serializer_valid(self):
        data = {
            "source": self.source_station.id,
            "destination": self.destination_station.id,
            "distance": 1,
        }
        serializer = RouteSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_route_serializer_invalid(self):
        data = {
            "source": self.source_station.id,
            "destination": self.source_station.id,
            "distance": 1,
        }
        serializer = RouteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Source and destination should be different",
        )


class TripSerializerTests(BaseTripTests):
    def setUp(self):
        super().setUp()
        self.crew_member = CrewMember.objects.create(
            first_name="Test", last_name="Testing"
        )

    def test_trip_serializer_valid(self):
        data = {
            "route": self.route.id,
            "train": self.train.id,
            "crew": [self.crew_member.id],
            "departure_time": timezone.now() + timedelta(hours=1),
            "arrival_time": timezone.now() + timedelta(hours=5),
        }
        serializer = TripSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_trip_serializer_invalid_departure_time(self):
        data = {
            "route": self.route.id,
            "train": self.train.id,
            "crew": [self.crew_member.id],
            "departure_time": timezone.now() - timedelta(hours=1),
            "arrival_time": timezone.now() + timedelta(hours=5),
        }
        serializer = TripSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["departure_time"][0],
            "Departure time must be in the future",
        )

    def test_trip_serializer_invalid_arrival_time(self):
        data = {
            "route": self.route.id,
            "train": self.train.id,
            "crew": [self.crew_member.id],
            "departure_time": timezone.now() + timedelta(hours=1),
            "arrival_time": timezone.now(),
        }
        serializer = TripSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["arrival_time"][0],
            "Arrival time must be after the departure time",
        )

    def test_trip_serializer_invalid_train(self):
        Trip.objects.create(
            route=self.route,
            train=self.train,
            departure_time=timezone.now() + timedelta(hours=1),
            arrival_time=timezone.now() + timedelta(hours=5),
        )
        data = {
            "route": self.route.id,
            "train": self.train.id,
            "crew": [self.crew_member.id],
            "departure_time": timezone.now() + timedelta(hours=2),
            "arrival_time": timezone.now() + timedelta(hours=4),
        }
        serializer = TripSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["train"][0],
            f"Train {self.train} is already assigned to another train during this time.",
        )

    def test_trip_serializer_invalid_crew(self):
        train = Train.objects.create(
            name="Second Train", car_num=1, places_in_car=10, train_type=self.train_type
        )

        trip = Trip.objects.create(
            route=self.route,
            train=train,
            departure_time=timezone.now() + timedelta(hours=1),
            arrival_time=timezone.now() + timedelta(hours=5),
        )
        trip.crew.set([self.crew_member])

        data = {
            "route": self.route.id,
            "train": self.train.id,
            "crew": [self.crew_member.id],
            "departure_time": timezone.now() + timedelta(hours=2),
            "arrival_time": timezone.now() + timedelta(hours=4),
        }
        serializer = TripSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["crew"][0],
            f"Crew member {self.crew_member} is already assigned to another trip during this time.",
        )
