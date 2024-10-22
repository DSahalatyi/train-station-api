from drf_spectacular.utils import extend_schema_view, extend_schema

trains_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Station"],
        description="Get a list of all trains",
    ),
    create=extend_schema(
        tags=["Station"],
        description="Add a new train",
    ),
)
