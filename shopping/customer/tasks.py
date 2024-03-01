
from celery import shared_task
from .models import MyUser
from django.core.mail import send_mail

@shared_task
def send_otp_email(user_id, opt_code):
    user = MyUser.objects.get(pk=user_id)
    send_mail(
        'Your OTP Code',
        f'Your OTP code is: {otp.code}',
        'fa.mahabadi@yahoo.com',
        [user.email],
        fail_silently=False,
    )
  
