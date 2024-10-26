from django.test import TestCase
from django.urls import reverse, resolve

from registration_service.views import (
    LoginView,
    RegistrationView,
    ResetView,
    PasswordConfirmView
)

class UrlsTestCase(TestCase):
    def test_login_url(self):
        name = 'login'
        path = reverse(name)
        self.assertEqual(
            resolve(path).func.view_class, LoginView
        )

    def test_reset_url(self):
        name = 'password_reset'
        path = reverse(name)
        self.assertEqual(
            resolve(path).func.view_class, ResetView
        )

    def test_reset_confirm_url(self):
        name = 'password_reset_confirm'
        path = reverse(name, kwargs=dict(uidb64=1, token=129312))
        self.assertEqual(
            resolve(path).func.view_class, PasswordConfirmView
        )

    def test_registration_url(self):
        name = 'registration'
        path = reverse(name)
        self.assertEqual(
            resolve(path).func.view_class, RegistrationView
        )