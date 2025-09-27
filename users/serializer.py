from rest_framework.serializers import ModelSerializer

from users.models import Payments


class PaymentsSerializer(ModelSerializer):
    """
    Serializer вывода платежей
    """

    class Meta:
        model = Payments
        fields = "__all__"
