from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User


class SubscriptionsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="tester@admin.py")
        self.course1 = Course.objects.create(
            name="1 тест", description="1", owner=self.user
        )

    def test_subscriptions_post(self):
        """Тестирование добавления и удаления подписки пользователя на курс."""

        url = reverse("users:subscription")

        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course1.pk}
        response = self.client.post(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("message"), "подписка добавлена")

        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course1.pk}
        response = self.client.post(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get("message"), "подписка удалена")
