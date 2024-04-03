from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Response, Advert
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import mail_managers

""" post_save запускает действие всякий раз, когда 
    пользователь сохраняет какой-либо объект в базе данных
  -- if created:   проверяет, создана модель или нет ----  
  --  create_advert: реагирует на создание нового объявления -- 
"""


@receiver(post_save, sender=Advert)
def create_advert(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.title} {instance.created.strftime("%Y-%M-%d")}')


@receiver(post_save, sender=Response)
def send_message_appointment(sender, instance, created, **kwargs):
    if created and instance.user.email:
        print(f'''Пользователь {instance.user.email}, откликнулся на ваш пост - '{instance.text}' ''')

        html_content = render_to_string('email_message.html', {'instance': instance, })

        msg = EmailMultiAlternatives(
            subject=f'Отклик на пост - {instance.text}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
