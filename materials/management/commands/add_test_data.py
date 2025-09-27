from django.core.management.base import BaseCommand
from django.db import connection

from materials.models import Course, Lesson
from users.models import User, Payments


class Command(BaseCommand):

    help = "Добавляет тестовые данные в базу данных для модели Payments"

    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE users_user RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE users_payments RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE materials_lesson RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE materials_course RESTART IDENTITY CASCADE;")

        user1, _ = User.objects.get_or_create(
            email="test1@mail.ru", phone="79876543210", city="Россия"
        )
        user2, _ = User.objects.get_or_create(
            email="test2@gmail.com", phone="01234567897", city="Германия"
        )

        course1, _ = Course.objects.get_or_create(
            name="Курс 1", description="Легкий курс"
        )
        course2, _ = Course.objects.get_or_create(
            name="Курс 2", description="Сложный курс"
        )

        payments = [
            {
                "user": user1,
                "paid_course": course1,
                "payment_method": "cash",
            },
            {
                "user": user2,
                "paid_course": course2,
                "payment_method": "transfer",
            },
        ]

        lessons = [
            {
                "name": "Python",
                "description": "Легкий урок",
                "course": course1,
            },
            {
                "name": "Java",
                "description": "Сложный урок",
                "course": course2,
            },
        ]

        for payments_data in payments:
            payment, created = Payments.objects.get_or_create(**payments_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Платеж добавлен"))

        for lessons_data in lessons:
            lesson, created = Lesson.objects.get_or_create(**lessons_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Урок добавлен: {lesson.name}"))
