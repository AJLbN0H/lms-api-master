from datetime import datetime, tzinfo
from django.utils import timezone
from celery import shared_task

from users.models import User


@shared_task
def blocking_inactive_users():
    """Блокирует пользователя, который не заходил в свой аккаунт больше месяца."""

    users = User.objects.all()

    time = datetime.now()

    time_a_month_earlier = time.month - 1

    new_time = time.replace(month=time_a_month_earlier)
    for user in users:
        if user.last_login:

            if timezone.is_aware(new_time):
                user_login = (
                    timezone.make_aware(user.last_login)
                    if timezone.is_naive(user.last_login)
                    else user.last_login
                )
            else:
                user_login = (
                    user.last_login.replace(tzinfo=None)
                    if timezone.is_aware(user.last_login)
                    else user.last_login
                )

            if user_login < new_time:
                user.is_active = False
                user.save()
