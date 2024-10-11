from django.core.exceptions import ValidationError
from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()

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

    def __str__(self):
        return f"{self.source.name} - {self.destination.name} ({str(self.distance)} km)"

    def clean(self):
        if self.source == self.destination:
            raise ValidationError("Source and destination should be different")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("source", "destination"),
                name="unique_route",
            )
        ]
