from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.serializers import (
    OrderSerializer,
    OrderListSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related(
                "tickets__trip__train",
                "tickets__trip__route__source",
                "tickets__trip__route__destination",
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ("list", "retrieve"):
            serializer = OrderListSerializer

        return serializer
