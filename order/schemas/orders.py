from drf_spectacular.utils import extend_schema_view, extend_schema

orders_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Order"],
        description="Get a list of all stations",
    ),
    create=extend_schema(
        tags=["Order"],
        description="Add a new station",
    )
)