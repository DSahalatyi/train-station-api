import django_filters

from station.models import Trip


class TripFilter(django_filters.FilterSet):
    from_ = django_filters.CharFilter(
        field_name="route__source__name", lookup_expr="iexact"
    )
    to = django_filters.CharFilter(
        field_name="route__destination__name", lookup_expr="iexact"
    )
    date = django_filters.DateFilter(
        field_name="departure_time", lookup_expr="date"
    )

    class Meta:
        model = Trip
        fields = ("from_", "to")

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            if "from" in data:
                data["from_"] = data["from"]
                del data["from"]

        super().__init__(data, *args, **kwargs)
