from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from order.models import Order, Ticket
from order.tests.base_test_cases import BaseTicketTests


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


class TicketModelTests(BaseTicketTests):
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
