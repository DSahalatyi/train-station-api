from django.urls import path

from user.jwt_views import (
    CustomTokenObtainPairView,
    TokenRefreshViewWithTag,
    TokenVerifyViewWithTag,
)
from user.views import CreateUserView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", ManageUserView.as_view(), name="manage"),
    # SimpleJWT
    path("tokens/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("tokens/refresh/", TokenRefreshViewWithTag.as_view(), name="token_refresh"),
    path("tokens/verify/", TokenVerifyViewWithTag.as_view(), name="token_verify"),
]
