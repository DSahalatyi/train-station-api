from drf_spectacular.utils import extend_schema_view, extend_schema

create_user_view_schema = extend_schema_view(
    post=extend_schema(
        tags=["User"],
        description="Create a new user",
    )
)

manage_user_view_schema = extend_schema_view(
    get=extend_schema(
        tags=["User"],
        description="Retrieve information about current user",
    ),
    put=extend_schema(
        tags=["User"],
        description="Update information about current user",
    ),
    patch=extend_schema(
        tags=["User"],
        description="Update information about current user",
    ),
)
