from django import forms
from todo.models import Cart, Lists, Boards


class CreateBoardForm(forms.Form):
    name = forms.CharField(max_length=20)
