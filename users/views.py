from django.shortcuts import get_object_or_404
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
from rest_framework.response import Response

from materials.models import Course
from users.models import Payments, User, Subscriptions
from users.serializer import PaymentsSerializer, UserSerializer, SubscriptionsSerializer


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
    """Generic создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод активации пользователя при создании его создании."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class SubscriptionsListApiView(ListAPIView):
    """Generic вывода списка уроков."""

    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

    def post(self, *args, **kwargs):
        """Метод добавления и удаления подписки у пользователя."""
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscriptions.objects.filter(user=user, course=course_item)

        if not subs_item.exists():
            new_subscription = Subscriptions.objects.create(
                user=user, course=course_item, subscription_sign=True
            )
            message = "подписка добавлена"
            new_subscription.save()

        else:
            subs_item.delete()
            message = "подписка удалена"

        return Response({"message": message})
