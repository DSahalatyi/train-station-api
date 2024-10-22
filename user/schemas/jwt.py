from drf_spectacular.utils import extend_schema_view, extend_schema

jwt_view_schema = extend_schema_view(post=extend_schema(tags=["User"]))
