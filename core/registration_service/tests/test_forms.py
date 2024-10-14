from django.test import TestCase

from core.registration_service.forms import (
    LoginForm,
    RegistrationForm,
    ResetForm,
    PasswordSetForm,
)
from core.registration_service.views import LoginView


class LoginFormTest(TestCase):
    def setUp(self):
        self.form = LoginForm(
            password='SomePassword312',
            username='admin',
            remember=True
        )

    def test_widgets(self):
        pass


class RegistrationFormTest(TestCase):
    pass

class ResetFormTest(TestCase):
    pass

class PasswordSetFormTest(TestCase):
    pass