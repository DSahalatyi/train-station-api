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
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshViewWithTag.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyViewWithTag.as_view(), name="token_verify"),
]
