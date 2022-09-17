from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth import password_validation
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from user.forms import LoginForm, RegisterForm, AuthenticateForm, ForgetPassForm, UserUpdateForm
from user.models import User, OTP, OTPType
from user.utils import sending_email


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        ctx = {"login_form": login_form}
        return render(request, "user/login.html", context=ctx)

    def post(self, request):
        login_form = LoginForm(request.POST)
        next_url = request.POST.get("next_url")
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                _login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("home")
            else:
                login_form.errors['user'] = 'اطلاعات ارسالی اشتباه است '
                return render(request, "user/login.html", {"login_form": login_form})
        else:
            login_form.errors['user'] = 'اطلاعات ارسالی اشتباه است '
            return render(request, "user/login.html", {"login_form": login_form})


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        ctx = {"register_form": register_form}
        return render(request, "user/register.html", context=ctx)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get("username")
            user = User.objects.get_or_create(username=email, is_email_verified=False)[0]
            code = OTP.objects.create(user=user, type=OTPType.AUTHENTICATE)
            if sending_email("your auth code (its expired 3 min later):", code.code, email):
                return redirect("authenticate")
            else:
                register_form.errors['email'] = ' مشکلی در ارسال ایمیل به وجود امد لطفا دوباره تلاش کنید'
                return render(request, "user/register.html", {"register_form": register_form})

        else:
            register_form.errors['email'] = 'ایمیل وجود دارد '
            return render(request, "user/register.html", {"register_form": register_form})


class AuthenticateView(View):

    def get(self, request):
        authenticate_form = AuthenticateForm()
        ctx = {"authenticate_form": authenticate_form}
        return render(request, "user/authenticate.html", context=ctx)

    def post(self, request):
        authenticate_form = AuthenticateForm(request.POST)
        if authenticate_form.is_valid():
            otp: OTP = authenticate_form.cleaned_data.get("code")
            user = otp.user
            user.is_email_verified = True
            try:
                password_validation.validate_password(authenticate_form.cleaned_data.get("password"), user=user)
            except BaseException:
                authenticate_form.errors["code"] = """
                                        1-این پسورد خیلی کوتاه است حداقل 8 کاراکتر
                                        2-پسورد خیلی ساده است
                                        3-پسورد فقط عدد است
                                        """
                return render(request, "user/authenticate.html", context={"authenticate_form": authenticate_form})
            user.set_password(authenticate_form.cleaned_data.get("password"))
            user.save()
            _login(request, user)
            request.session["username"] = user.username
            return redirect("home")

        else:

            return render(request, "user/authenticate.html", context={"authenticate_form": authenticate_form})


class ForgetPasswordView(View):
    def get(self, request):
        forget_pass_form = ForgetPassForm()
        ctx = {"password_form": forget_pass_form}
        return render(request, "user/password.html", context=ctx)

    def post(self, request):
        forget_pass_form = ForgetPassForm(request.POST)
        if forget_pass_form.is_valid():
            user = forget_pass_form.cleaned_data.get("email")
            code = OTP.objects.create(user=user, type=OTPType.FORGETPASSWORD)
            if sending_email("your auth code (its expired 3 min later):", code.code, user.username):
                return redirect("authenticate")
            else:
                forget_pass_form.errors['pass'] = ' مشکلی در ارسال ایمیل به وجود امد لطفا دوباره تلاش کنید'
                return render(request, "user/password.html", {"password_form": forget_pass_form})

        else:
            forget_pass_form.errors['pass'] = 'ایمیل وجود ندارد '
            return render(request, "user/password.html", {"password_form": forget_pass_form})


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ProfileView(View):

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        ctx = {"form": form}
        return render(request, "user/profile.html", context=ctx)

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        else:
            return redirect("profile", kwargs={"form": form})


def logout(request):
    _logout(request)
    return redirect('home')
