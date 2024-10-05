from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from booking.models import Campus, Audience
from booking.forms import ReservationForm


class CampusListView(ListView):
    model = Campus
    template_name = 'booking/main_func/campus_list.html'
    context_object_name = 'campuses'
    queryset = Campus.objects.all()

    # TODO: прописать отображение кампуса к url главной страницы,
    #  отобразить информацию для Frontend


class AudienceListView(ListView):
    model = Audience
    template_name = 'booking/main_func/audience_list.html'
    context_object_name = 'audiences'

    def get_queryset(self):
        campus = None
        return Audience.objects.filter(campus=campus)

        # TODO: Дописать query

    # TODO: Отобразить информацию для Frontend


class AudienceDetailView(FormMixin, DetailView):
    model = Audience
    pk_url_kwarg = 'audience_id'
    context_object_name = 'audience'
    template_name = 'booking/main_func/audience_detail.html'
    form_class = ReservationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['audience'] = None
        return kwargs

        # TODO Дописать kwargs['audience']

    def get_success_url(self):
        pass

        # TODO дописать get_success_url

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_object(self, **kwargs):
        audience = None
        return Audience.objects.prefetch_related().get(pk=audience)

        # TODO: Дописать query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = None
        context['form'] = self.get_form()
        return context

        # TODO: Дописать context['reservations']

    # TODO: Отобразить информацию для Frontend
