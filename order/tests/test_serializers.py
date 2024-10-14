from order.serializers import TicketSerializer
from order.tests.base_test_cases import BaseTicketTests


class TicketSerializerTests(BaseTicketTests):
    def test_ticket_serializer_valid(self):
        data = {"car": 1, "place": 1, "trip": self.trip.id, "order": self.order.id}
        serializer = TicketSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_ticket_serializer_invalid_place(self):
        data = {"car": 1, "place": 11, "trip": self.trip.id, "order": self.order.id}
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["place"][0],
            f"place number must be in available range: (1, places_in_car): (1, {self.train.places_in_car})",
        )

    def test_ticket_serializer_invalid_car(self):
        data = {"car": 2, "place": 1, "trip": self.trip.id, "order": self.order.id}
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["car"][0],
            f"car number must be in available range: (1, car_num): (1, {self.train.car_num})",
        )
