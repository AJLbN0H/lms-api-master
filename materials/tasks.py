from celery import shared_task
from django.core.mail import send_mail

from users.models import Subscriptions

@shared_task
def checking_for_rate_updates(pk):
    subscriptions = Subscriptions.objects.all()
    users_list = []
    for user in subscriptions:
        if user.course_id == pk:
            if user.subscription_sign:
                users_list.append(user.user.email)

    subject = f"Курс на который вы были подписаны обновился"
    message = "Зайдите на наш сайт, чтобы увидеть изменения"
    from_email = "Sasha.kel-1@yandex.ru"
    recipient_list = users_list
    send_mail(subject, message, from_email, recipient_list)