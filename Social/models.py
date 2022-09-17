from django.db import models
from django.utils.translation import gettext as _
from user.models import User
from todo.models import Cart


class Comment(models.Model):
    text = models.CharField(max_length=255, verbose_name=_("text"))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("user"))
    cards = models.ForeignKey(Cart, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("cards"),
                              related_name="comment_cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:10]
