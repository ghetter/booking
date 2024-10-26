from django.urls import path

from registration_service.views import LoginView, RegistrationView, ResetView, PasswordConfirmView


urlpatterns = [
    path(
        '',
         LoginView.as_view(),
        name='login'
    ),
    path(
        'create/',
        RegistrationView.as_view(),
        name='registration'
    ),
    path(
        'reset/',
        ResetView.as_view(),
        name='password_reset'
    ),
    path(
        'reset-confirm/<uidb64>/<token>/',
        PasswordConfirmView.as_view(),
        name='password_reset_confirm'
    )
]