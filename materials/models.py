from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Название", help_text="Введите название курса"
    )
    preview = models.ImageField(
        upload_to="materials/",
        verbose_name="Превью",
        null=True,
        blank=True,
        help_text="Загрузите картинку",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Название", help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    preview = models.ImageField(
        upload_to="materials/",
        verbose_name="Превью",
        null=True,
        blank=True,
        help_text="Загрузите картинку",
    )
    link_to_the_video = models.CharField(
        max_length=300,
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Вставте ссылку на видео",
    )
    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        on_delete=models.SET_NULL,
        help_text="Выберите курс",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
