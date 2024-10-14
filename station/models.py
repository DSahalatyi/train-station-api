import pathlib
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"],
                name="unique_coordinates"
            )
        ]

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, on_delete=models.RESTRICT, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.RESTRICT, related_name="destination_routes"
    )
    distance = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("source", "destination"),
                name="unique_route",
            )
        ]

    @staticmethod
    def validate_source_destination(source, destination, error_to_raise):
        if source == destination:
            raise error_to_raise("Source and destination should be different")

    def __str__(self):
        return f"{self.source.name} - {self.destination.name} ({str(self.distance)} km)"

    def clean(self):
        self.validate_source_destination(self.source, self.destination, ValidationError)


class TrainType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=63, unique=True)
    car_num = models.IntegerField(validators=[MinValueValidator(1)])
    places_in_car = models.IntegerField(validators=[MinValueValidator(1)])
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="trains"
    )

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    filename = (
        f"{slugify(instance.full_name)}-{uuid.uuid4()}.jpg"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/crew/") / pathlib.Path(filename)


class CrewMember(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    image = models.ImageField(null=True, upload_to=get_image_path)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="trips")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="trips")
    crew = models.ManyToManyField(CrewMember, related_name="trips")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.departure_time} | {self.route} | {self.train}"
