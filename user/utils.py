import random
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


def sending_email(subject, text, receiver):
    try:
        send_mail(subject, text, settings.EMAIL_HOST_USER, [receiver])
        return True
    except BaseException:
        return False


def create_otp_code():
    from user.models import OTP
    choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while True:
        code = random.choices(choices, k=settings.OTP_SETTINGS["CODE_LEN"])
        code_str = "".join(code)
        refs = OTP.objects.filter(code=code_str).exists()
        if not refs:
            break

    return code_str


def create_end_time():
    return timezone.now() + timedelta(minutes=3)
