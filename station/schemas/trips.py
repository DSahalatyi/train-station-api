from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

trips_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Station"],
        description="Get a list of all trips",
        parameters=[
            OpenApiParameter(
                name="from_",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter trips by station of departure. "
                "Example: ?from=Kyiv | ?from_=Kyiv",
                required=False,
            ),
            OpenApiParameter(
                name="to",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter trips by station of arrival. Example: ?to=Kyiv",
                required=False,
            ),
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter trips by date of departure. Date format: YYYY-MM-DD "
                            "Example: ?date=2024-01-01",
                required=False,
            ),
        ],
    ),
    create=extend_schema(
        tags=["Station"],
        description="Add a new trip",
    ),
    retrieve=extend_schema(
        tags=["Station"],
        description="Retrieve a trip",
    ),
    update=extend_schema(
        tags=["Station"],
        description="Update a trip",
    ),
    partial_update=extend_schema(
        tags=["Station"],
        description="Update a trip",
    ),
    destroy=extend_schema(
        tags=["Station"],
        description="Delete a trip",
    ),
    upload_image=extend_schema(
        tags=["Station"],
        description="Upload an image of a trip",
    ),
)
