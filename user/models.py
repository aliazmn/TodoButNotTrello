from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

from user.utils import create_otp_code , create_end_time
from user.manager import CustomUserManager


class OTPType(models.IntegerChoices):
    AUTHENTICATE = (1, _("AUTHENTICATE"))
    FORGETPASSWORD = (2, _("FORGETPASSWORD"))


class User(AbstractUser):
    username = models.EmailField(verbose_name=_('Username'), unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    is_email_verified = models.BooleanField(null=True, blank=True)
    phone_number = models.CharField(max_length=19, null=True, blank=True)

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username


class OTP(models.Model):
    code = models.CharField(max_length=11, default=create_otp_code, verbose_name=_("code"), unique=True)
    exp_time = models.DateTimeField(default=create_end_time, verbose_name=_("exp_time"))
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="otp_user", verbose_name=_("user"))
    type = models.IntegerField(choices=OTPType.choices, verbose_name=_("type"))

    @property
    def is_expired(self):
        if self.exp_time < timezone.now():
            return True
        return False

    def __str__(self):
        return self.code
