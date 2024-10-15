from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm, UsernameField, PasswordResetForm, SetPasswordForm



class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class' : "form__input username",
                "placeholder" : "Логин"
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class" : "form__input password",
                "placeholder" : "Пароль"
            }
        ),
    )
    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs=dict(name="rememberPass", id="rememberPassID", value="YesRemember"),
        )
    )

class RegistrationForm(BaseUserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'id' : 'email',
                'class' : 'form__input email',
                'placeholder' : 'Введите почту'
            }
        ),
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'id' : 'fname',
                'class' : 'form__input fname',
                'placeholder' : 'Введите имя'
            }
        ),
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'id': 'login',
                'class': 'form__input username',
                'placeholder' : 'Введите логин'
            }
        ),
    )
    password1 = forms.CharField(
        label='Введите пароль',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id' : 'password',
                'class' : 'form__input password',
                'placeholder' : 'Введите пароль'
            }
        ),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'repassword',
                'class': 'form__input password',
                'placeholder' : 'Повторите пароль'
            }
        ),
    )
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

class ResetForm(PasswordResetForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'id' : 'email',
                'class': "form__input password",
                'placeholder': "Введите почту"
            }
        )
    )

class PasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
                'class': 'form__input password',
                'placeholder': 'Введите пароль'
            }
        ),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'repassword',
                'class': 'form__input password',
                'placeholder': 'Повторите пароль'
            }
        ),
    )


