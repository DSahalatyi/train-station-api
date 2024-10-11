from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import IntegerField, ForeignKey

from station.models import Trip


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ticket(models.Model):
    car = IntegerField(validators=[MinValueValidator(1)])
    seat = IntegerField(validators=[MinValueValidator(1)])
    trip = ForeignKey(Trip, on_delete=models.RESTRICT, related_name="tickets")
    order = ForeignKey(Order, on_delete=models.RESTRICT, related_name="tickets")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["car", "seat", "trip"],
                name="unique_ticket"
            )
        ]
