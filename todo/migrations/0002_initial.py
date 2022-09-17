# Generated by Django 4.0.5 on 2022-06-04 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workspace_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='workspace',
            name='cards',
            field=models.ManyToManyField(to='todo.cart'),
        ),
        migrations.AddField(
            model_name='workspace',
            name='members',
            field=models.ManyToManyField(related_name='workspace_members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category', to='todo.subject', verbose_name='Subject'),
        ),
    ]
