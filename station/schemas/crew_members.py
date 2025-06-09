from drf_spectacular.utils import extend_schema_view, extend_schema

crew_members_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Station"],
        description="Get a list of all crew members",
    ),
    create=extend_schema(
        tags=["Station"],
        description="Add a new crew member",
    ),
    retrieve=extend_schema(
        tags=["Station"],
        description="Retrieve a crew member",
    ),
    update=extend_schema(
        tags=["Station"],
        description="Update a crew member",
    ),
    partial_update=extend_schema(
        tags=["Station"],
        description="Update a crew member",
    ),
    destroy=extend_schema(
        tags=["Station"],
        description="Delete a crew member",
    ),
    upload_image=extend_schema(
        tags=["Station"],
        description="Upload an image of a crew member",
    ),
)
