from django.shortcuts import get_object_or_404
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course
from users.models import Payments, User, Subscriptions


class PaymentsSerializer(ModelSerializer):
    """Serializer вывода платежей."""

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Serializer вывода пользователей."""

    class Meta:
        model = User
        fields = "__all__"


class SubscriptionsSerializer(ModelSerializer):
    """Serializer вывода подписки."""

    subscription_sign = SerializerMethodField()

    def get_subscription_sign(self, obj):
        user = self.context["request"].user
        return Subscriptions.objects.filter(user=user, course=obj.course).exists()

    class Meta:
        model = Subscriptions
        fields = ("user", "course", "subscription_sign")
