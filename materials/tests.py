from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course
from users.models import User


class LessonTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="tester1@admin.py")
        self.course = Course.objects.create(
            name="Тестирование всего", description="1", owner=self.user1
        )
        self.lesson = Lesson.objects.create(
            name="Тестирование ПО",
            description="1",
            owner=self.user1,
            course=self.course,
        )

        self.user2 = User.objects.create(email="tester2@admin.py")

        self.user3 = User.objects.create(email="moder@admin.py")
        moderators_group, created = Group.objects.get_or_create(name="Модераторы")
        self.user3.groups.add(moderators_group)

    def test_lesson_retrieve(self):
        """Тестирование получения подробной информации о уроке."""

        url = reverse("materials:lessons-retrieve", args=(self.lesson.pk,))

        self.client.force_authenticate(user=self.user1)
        response1 = self.client.get(url)
        data1 = response1.json()
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(data1.get("name"), self.lesson.name)

        self.client.force_authenticate(user=self.user2)
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user3)
        response3 = self.client.get(url)
        data3 = response3.json()
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(data3.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создания урока."""

        url = reverse("materials:lessons-create")

        self.client.force_authenticate(user=self.user1)
        data1 = {
            "name": "Testing-1",
        }
        response1 = self.client.post(url, data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

        self.client.force_authenticate(user=self.user2)
        data = {
            "name": "Testing-11",
            "link_to_the_video": "https://my.sky.pro/student-cabinet/stream-lesson/154298/homework-requirements",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 2)

        self.client.force_authenticate(user=self.user3)
        data2 = {
            "name": "Testing-2",
        }
        response2 = self.client.post(url, data2)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование обновления информации урока."""

        url = reverse("materials:lessons-update", args=(self.lesson.pk,))

        self.client.force_authenticate(user=self.user1)
        data1 = {"name": "Тестирование patch"}
        response1 = self.client.patch(url, data1)
        data_1 = response1.json()
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(data_1.get("name"), "Тестирование patch")

        self.client.force_authenticate(user=self.user2)
        data2 = {"name": "Тестирование patch1"}
        response2 = self.client.patch(url, data2)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user3)
        data3 = {"name": "Тестирование patch2"}
        response3 = self.client.patch(url, data3)
        data_3 = response3.json()
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(data_3.get("name"), "Тестирование patch2")

    def test_lesson_list(self):
        """Тестирование получения списка уроков."""

        url = reverse("materials:lessons-list")

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link_to_the_video": None,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user1.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(data, result)

    def test_lesson_delete(self):
        """Тестирование удаления урока."""

        url = reverse("materials:lessons-delete", args=(self.lesson.pk,))

        self.client.force_authenticate(user=self.user2)
        response2 = self.client.delete(url)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

        self.client.force_authenticate(user=self.user3)
        response3 = self.client.delete(url)
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

        self.client.force_authenticate(user=self.user1)
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
