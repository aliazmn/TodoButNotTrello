# Generated by Django 4.0.5 on 2022-06-10 08:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_is_mobile_verified_user_is_email_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='exp_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 10, 8, 5, 15, 828951, tzinfo=utc), verbose_name='exp_time'),
        ),
    ]