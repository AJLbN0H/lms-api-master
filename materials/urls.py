from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView,
    LessonDestroyApiView,
)

app_name = "materials"

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons-list"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons-retrieve"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons-update"
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons-delete",
    ),
] + router.urls
