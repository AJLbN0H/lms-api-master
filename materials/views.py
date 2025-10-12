from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginations import CustomPagination
from materials.permissions import IsModer, IsOwner
from materials.serializer import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)


class CourseViewSet(ModelViewSet):
    """ViewSet курсов."""

    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """Получение нужного сериалайзера."""
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """Метод проверки прав доступа."""
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле owner на текущего авторизованного пользователя."""
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """Generic вывода списка уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonCreateApiView(CreateAPIView):
    """Generic создания урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """Метод переопределяющий при создании урока поле owner на текущего авторизованного пользователя."""
        serializer.save(owner=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    """Generic просмотра детальной информации урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    """Generic обновления информации урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    """Generic удаления урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer | IsOwner]
