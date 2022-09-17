from django.db import models
from django.utils import timezone
from user.models import User
from django.utils.translation import gettext as _
from django.shortcuts import reverse


class Boards(models.Model):
    name = models.CharField(max_length=64, verbose_name=_("name"))
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name="workspace_admin")
    members = models.ManyToManyField(User, related_name="board_member", blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list", args=[self.id])


class Lists(models.Model):
    title = models.CharField(max_length=64)
    board = models.ForeignKey(Boards, on_delete=models.PROTECT, related_name="list_board", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    name = models.CharField(max_length=64, verbose_name=_("name"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_time = models.DateField(null=True, blank=True)
    is_finished = models.BooleanField(default=False, verbose_name=_("is_finished"))
    desc = models.TextField(default="Add a more detailed description... ")
    members = models.ManyToManyField(User, related_name="cart_member", blank=True)
    list = models.ForeignKey(Lists, on_delete=models.PROTECT, related_name="cart_list", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("carts", args=[self.id])
