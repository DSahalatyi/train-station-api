from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import IntegerField, ForeignKey

from station.models import Trip


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ticket(models.Model):
    car = IntegerField(validators=[MinValueValidator(1)])
    place = IntegerField(validators=[MinValueValidator(1)])
    trip = ForeignKey(Trip, on_delete=models.RESTRICT, related_name="tickets")
    order = ForeignKey(Order, on_delete=models.RESTRICT, related_name="tickets")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["car", "place", "trip"], name="unique_ticket"
            )
        ]

    def clean(self):
        self.validate_place_car(
            car=self.car,
            place=self.place,
            trip=self.trip,
            error_to_raise=ValidationError,
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @staticmethod
    def validate_place_car(
        car,
        place,
        trip,
        error_to_raise,
    ):
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (car, "car", "car_num"),
            (place, "place", "places_in_car"),
        ]:
            count_attrs = getattr(trip.train, train_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {train_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )
