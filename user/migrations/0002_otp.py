# Generated by Django 4.0.5 on 2022-06-04 11:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import user.utils


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=user.utils.create_otp_code, max_length=11, unique=True, verbose_name='code')),
                ('exp_time', models.DateTimeField(default=datetime.datetime(2022, 6, 4, 11, 4, 51, 469957, tzinfo=utc), verbose_name='exp_time')),
                ('type', models.IntegerField(choices=[(1, 'AUTHENTICATE'), (2, 'FORGETPASSWORD')], verbose_name='type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='otp_user', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
