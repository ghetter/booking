from django.urls import reverse_lazy
from django.contrib.auth import views

from django.views.generic.edit import FormView


from registration_service.forms import LoginForm, RegistrationForm, ResetForm, PasswordSetForm

class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'registration_service/main_func/login.html'
    next_page = reverse_lazy('campus_list_view')

class RegistrationView(FormView):
    template_name = "registration_service/main_func/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ResetView(views.PasswordResetView):
    template_name = "registration_service/main_func/reset.html"
    form_class = ResetForm
    success_url = reverse_lazy('login')

class PasswordConfirmView(views.PasswordResetConfirmView):
    form_class = PasswordSetForm
    template_name = "registration_service/main_func/reset_confirm.html"
    success_url = reverse_lazy('login')











