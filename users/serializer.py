from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class PaymentsSerializer(ModelSerializer):
    """Serializer вывода платежей."""

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Serializer вывода платежей."""

    class Meta:
        model = User
        fields = "__all__"
