from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """Serializer вывода курсов."""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Serializer, который дополнительно выводит количество уроков определенного курса и выводит детальную инфу этих уроков."""

    number_of_lessons = SerializerMethodField()
    lessons = CourseSerializer(source="lesson_set", many=True, read_only=True)

    def get_number_of_lessons(self, course):
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = ("name", "preview", "description", "number_of_lessons", "lessons")


class LessonSerializer(ModelSerializer):
    """Serializer вывода уроков."""

    class Meta:
        model = Lesson
        fields = "__all__"
