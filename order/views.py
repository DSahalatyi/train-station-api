from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from order.models import Order
from order.schemas.orders import orders_viewset_schema
from order.serializers import (
    OrderSerializer,
    OrderListSerializer,
)


@orders_viewset_schema
class OrderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related(
                "tickets__trip__train",
                "tickets__trip__route__source",
                "tickets__trip__route__destination",
            ).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ("list", "retrieve"):
            serializer = OrderListSerializer

        return serializer
