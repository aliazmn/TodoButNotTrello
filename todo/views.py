from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from todo.models import Cart, Lists, Boards
from todo.forms import CreateBoardForm
from user.models import User
from Social.models import Comment
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


class HomeView(View):

    def get(self, request):
        ctx = {}

        if request.session.get("err"):
            err = request.session.get("err")
            ctx["err"] = err["name"][0]
            request.session["err"] = ""
        if request.user.is_authenticated:
            boards = Boards.objects.filter(members__id=request.user.id)
            lst_obj = []
            for elm in boards:
                lst_obj.append(elm)

            ctx["boards"] = lst_obj

        else:
            ctx["boards"] = []

        return render(request, "boards.html", context=ctx)

    @method_decorator(login_required(login_url="/login/"), name="dispatch")
    def post(self, request):
        data = CreateBoardForm(request.POST)
        if data.is_valid():
            new_board = Boards.objects.create(name=data.cleaned_data.get("name"), admin=request.user)
            new_board.members.add(request.user)
            new_board.save()
            return redirect("home")

        else:
            request.session["err"] = data.errors
            return redirect("home")


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ListView(View):
    def get(self, request, id):
        ctx = {"data": {}, "err": ""}
        if request.session.get("err"):
            err = request.session.get("err")
            ctx["err"] = err["name"][0]
            request.session["err"] = ""

        board = Boards.objects.filter(id=id, members__id=request.user.id, is_active=True).first()
        if not board:
            ctx['err'] = "wrong id"
            return render(request, 'lists.html', context=ctx)
        ctx["board"] = board
        lists = Lists.objects.filter(board=board)
        if lists:

            for elm in lists:
                lst_cart = []
                carts = elm.cart_list.all()
                for item in carts:
                    lst_cart.append(item)
                ctx["data"][elm] = lst_cart
        return render(request, 'lists.html', context=ctx)

    def post(self, request, id):
        cart_name = request.POST.get("cart_name")
        list_name = request.POST.get("list_name")

        if cart_name and not list_name:
            _list = Lists.objects.filter(id=id).first()
            if not _list:
                return HttpResponse("list not found")
            new_cart = Cart.objects.create(
                name=cart_name,
                list=_list
            )
            return redirect("list", id=_list.board_id)

        else:
            new_list = Lists.objects.create(
                title=list_name,
                board_id=id
            )
            return redirect("list", id=id)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class CartView(View):

    def get(self, request, id):
        ctx = {"cart": "", "list": "", "board": "", "comment": [], "members": [], }
        carts = Cart.objects.filter(
            id=id
        ).first()
        lst_comments, lst_user_exclude, lst_member = [], [], []

        comments = carts.comment_cart.all()
        members = carts.members.all()
        for item in comments:
            lst_comments.append(item)
        for st in members:
            lst_member.append(st)
            lst_user_exclude.append(st.id)

        ctx["cart"] = carts
        ctx["list"] = carts.list
        ctx["board"] = carts.list.board
        ctx["comment"] = lst_comments
        ctx["members"] = lst_member
        ctx["user"] = User.objects.exclude(id__in=lst_user_exclude)
        ctx["login_user"] = request.user
        ctx["date"] = carts.end_time  # TODO convert date in template #
        return render(request, "taskModify.html", context=ctx)

    def post(self, request, id):
        cart_obj = Cart.objects.filter(id=id).first()
        desc = request.POST.get("desc", "")
        end_time = request.POST.get("end_time", "")
        if desc:
            cart_obj.desc = desc
            cart_obj.save()
        if end_time:
            cart_obj.end_time = end_time
            cart_obj.save()
        return redirect("carts", id=id)


def add_user(request, cart_id, user_id):
    cart_obj = Cart.objects.filter(id=cart_id).first()
    user = User.objects.filter(id=user_id).first()
    cart_obj.members.add(user)
    cart_obj.list.board.members.add(user)
    cart_obj.save()

    return redirect("carts", id=cart_id)


def delete_user(request, cart_id, user_id):
    cart_obj = Cart.objects.filter(id=cart_id).first()
    user = User.objects.filter(id=user_id).first()
    cart_obj.members.remove(user)
    cart_obj.list.board.members.add(user)
    cart_obj.save()

    return redirect("carts", id=cart_id)


def comment_creator(request, id):
    text = request.POST.get("comment_text")
    cm_obj = Comment.objects.create(
        text=text,
        cards_id=id,
        user=request.user
    )
    return redirect("carts", id=id)


def delete_cart(request, cart_id, board_id):
    Cart.objects.get(id=cart_id).delete()
    return redirect("list", id=board_id)


@require_http_methods(["POST"])
@csrf_exempt
def change_name(request):
    body = json.loads(request.body.decode('utf-8'))
    model_name = body.get("model_name")
    model_id = body.get("id")
    data = body.get("name")
    if model_name == "board":
        obj = Boards.objects.filter(id=model_id).first()
        obj.name = data
        obj.save()
        return redirect("list", id=model_id)
    if model_name == "list":
        obj = Lists.objects.filter(id=model_id).first()
        obj.title = data
        obj.save()
        return redirect("list", id=obj.board_id)

    if model_name == "cart":
        obj = Cart.objects.filter(id=model_id).first()
        obj.name = data
        obj.save()
        return redirect("carts", id=model_id)

    else:
        return redirect("carts", id=model_id)