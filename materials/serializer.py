from PIL.Image import blend
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_link_to_the_video


class CourseSerializer(serializers.ModelSerializer):
    """Serializer вывода курсов."""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer, который дополнительно выводит количество уроков определенного курса и выводит детальную инфу этих уроков."""

    number_of_lessons = SerializerMethodField()
    lessons = CourseSerializer(source="lesson_set", many=True, read_only=True)

    def get_number_of_lessons(self, course):
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = ("name", "preview", "description", "number_of_lessons", "lessons")


class LessonSerializer(serializers.ModelSerializer):
    """Serializer вывода уроков."""

    link_to_the_video = serializers.CharField(
        validators=[validate_link_to_the_video], required=False
    )

    class Meta:
        model = Lesson
        fields = "__all__"
