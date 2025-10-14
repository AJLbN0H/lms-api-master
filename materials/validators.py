from rest_framework.serializers import ValidationError


def validate_link_to_the_video(value):
    """Проверяет, оставил ли пользователь ссылку на youtube.com."""

    if "https://www.youtube.com" not in value.lower():
        raise ValidationError("Можно указывать ссылку только на youtube.com")
