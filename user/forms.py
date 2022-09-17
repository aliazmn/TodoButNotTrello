from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm

from user.models import User, OTP, OTPType


class LoginForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'e-field-inner', 'placeholder': "نام کاربری خود را وارد کنید"}),
        label='نام کاربری')
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'e-field-inner', 'placeholder': "رمز عبور خود را وارد کنید"}),
                               label='رمز عبور')


class AuthenticateForm(forms.Form):
    code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': "e-field-inner"}), label="کد")
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'e-field-inner'}),
                               label="کلمه عبور")
    re_password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'e-field-inner'}),
                                  label="تکرار کلمه عبور")

    def clean_code(self):
        code = self.cleaned_data.get("code")
        otp_obj = OTP.objects.filter(code=code).first()
        if not otp_obj:
            raise forms.ValidationError("کد وجود ندارد")
        if otp_obj.is_expired:
            raise forms.ValidationError("out of time")

        return otp_obj

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password


class RegisterForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'e-field-inner', 'placeholder': "ایمیل خود را وارد کنید"}),
        label='ایمیل')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exists_user_by_email = User.objects.filter(username=username, is_email_verified=True).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')
        return username


class ForgetPassForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'e-field-inner'}))

    def clean_email(self):
        user_obj = User.objects.filter(username=self.cleaned_data.get("email"), is_email_verified=True,
                                       is_active=True).first()
        if not user_obj:
            raise forms.ValidationError("not exist")
        return user_obj


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'e-field-inner'}),
            'first_name': forms.TextInput(attrs={'class': 'e-field-inner'}),
            'last_name': forms.TextInput(attrs={'class': 'e-field-inner'}),
            'phone_number': forms.TextInput(attrs={'class': 'e-field-inner'}),

        }
