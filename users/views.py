from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializer import PaymentsSerializer, UserSerializer


class PaymentsListApiView(ListAPIView):
    """Generic вывода списка платежей."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson")
    ordering_fields = ["payment_date"]


class PaymentsCreateApiView(CreateAPIView):
    """Generic создания платежа."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsRetrieveApiView(RetrieveAPIView):
    """Generic просмотра детальной информации о платеже."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsUpdateApiView(UpdateAPIView):
    """Generic обновления информации о платеже."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentsDestroyApiView(DestroyAPIView):
    """Generic удаления платежа."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class UserCreateApiView(CreateAPIView):
    """Generic создания пользовтеля"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод активации пользователя при создании его создании."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
