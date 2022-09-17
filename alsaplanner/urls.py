from django.contrib import admin
from django.urls import path
from user import views as user_view
from todo import views as todo_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", user_view.LoginView.as_view(), name="login"),
    path("register/", user_view.RegisterView.as_view(), name="register"),
    path("authenticate/", user_view.AuthenticateView.as_view(), name="authenticate"),
    path("forget_password/", user_view.ForgetPasswordView.as_view(), name="forget_password"),
    path("profile/", user_view.ProfileView.as_view(), name="profile"),
    path("logout/", user_view.logout, name="logout"),

    path("", todo_view.HomeView.as_view(), name="home"),
    path("lists/<int:id>/", todo_view.ListView.as_view(), name="list"),
    path("carts/<int:id>/", todo_view.CartView.as_view(), name="carts"),
    path("add_member/<int:cart_id>/<int:user_id>", todo_view.add_user, name="add_member"),
    path("remove_member/<int:cart_id>/<int:user_id>", todo_view.delete_user, name="remove_member"),
    path("comment/<int:id>/", todo_view.comment_creator, name="comments"),
    path("delete_cart/<int:cart_id>/<int:board_id>", todo_view.delete_cart, name="delete"),
    path("change_name/", todo_view.change_name, name="change_name"),

]
