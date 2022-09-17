from celery import shared_task
from todo.models import Cart
from user.utils import sending_email
from django.utils import timezone
from datetime import timedelta


@shared_task(name="notify")
def notify():
    carts = Cart.objects.all()
    for elm in carts:
        if timezone.now() + timedelta(days=1) == elm.end_time:
            for item in elm.members.all():
                sending_email("your auth code (its expired 3 min later):", f"your {elm.name} is ranning out of time",
                              item.username)


#celery -A alsaplanner worker -l info
#celery -A alsaplanner beat -l info -S django