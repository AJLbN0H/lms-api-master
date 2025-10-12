from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (
    PaymentsListApiView,
    PaymentsCreateApiView,
    PaymentsUpdateApiView,
    PaymentsRetrieveApiView,
    PaymentsDestroyApiView,
    UserCreateApiView, SubscriptionsListApiView,
)

app_name = "users"

urlpatterns = [
    path("payments/", PaymentsListApiView.as_view(), name="payments_list"),
    path("payments/create/", PaymentsCreateApiView.as_view(), name="payments_create"),
    path(
        "payments/<int:pk>", PaymentsRetrieveApiView.as_view(), name="payments_retrieve"
    ),
    path("payments/<int:pk>/update/", PaymentsUpdateApiView.as_view(), name="v_update"),
    path(
        "payments/<int:pk>/delete/",
        PaymentsDestroyApiView.as_view(),
        name="payments_delete",
    ),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "subscription/",
        SubscriptionsListApiView.as_view(permission_classes=(AllowAny,)),
        name="subscription",
    ),
]
