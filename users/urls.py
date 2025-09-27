from django.urls import path

from users.views import (
    PaymentsListApiView,
    PaymentsCreateApiView,
    PaymentsUpdateApiView,
    PaymentsRetrieveApiView,
    PaymentsDestroyApiView,
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
]
