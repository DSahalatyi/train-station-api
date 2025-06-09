from django.test import TestCase

from station.models import Station, Route, TrainType, Train


class BaseTripTests(TestCase):
    def setUp(self):
        source_station = Station.objects.create(
            name="Source Station", latitude=1, longitude=1
        )
        destination_station = Station.objects.create(
            name="Destination Station", latitude=2, longitude=2
        )
        self.route = Route.objects.create(
            source=source_station, destination=destination_station, distance=1
        )
        self.train_type = TrainType.objects.create(name="Test")
        self.train = Train.objects.create(
            name="Test Train", car_num=1, places_in_car=10, train_type=self.train_type
        )