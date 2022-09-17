# Generated by Django 4.0.5 on 2022-07-01 10:44

from django.db import migrations, models
import user.utils


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_otp_exp_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='exp_time',
            field=models.DateTimeField(default=user.utils.create_end_time, verbose_name='exp_time'),
        ),
    ]