# Generated by Django 4.0.5 on 2022-06-10 15:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_otp_exp_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='exp_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 10, 15, 41, 2, 813424, tzinfo=utc), verbose_name='exp_time'),
        ),
    ]