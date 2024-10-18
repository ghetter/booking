from datetime import datetime, timedelta, date, time

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from booking.models import Campus, Audience
from booking.forms import ReservationForm

from booking.models import Reservation
from booking.mixins import LessonMixin

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
        campus = Campus.objects.get(id=self.kwargs['campus'])
        return Audience.objects.filter(campus=campus)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        floors = self.object_list.values_list('floor', flat=True).order_by().distinct()
        context['floors'] = floors
        return context
    # TODO: Отобразить информацию для Frontend


class AudienceDetailView(LessonMixin, FormMixin, DetailView):
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
        self.object = self.get_object()
        kwargs['audience'] = self.object
        return kwargs
        # TODO Дописать kwargs['audience']

    def get_success_url(self):
        return reverse_lazy('audience_detail', kwargs={'campus' : self.object.campus.id, 'audience_id' : self.object.id})

        # TODO дописать get_success_url

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_object(self, **kwargs):
        audience = self.kwargs[self.pk_url_kwarg]
        return Audience.objects.get(pk=audience)

        # TODO: Дописать query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        _date = self.get_date_from_query_params(self.request)
        reservations = self.object.reservations.filter(
            time_start__week=_date.isocalendar().week,
            time_end__week=_date.isocalendar().week
        )
        context['reservations'] = reservations
        context['form'] = self.get_form()

        context['date'] = self.get_the_range_of_the_week_str(_date)
        context['days'] = self.get_days(_date)
        context['class_time'] = self.get_class_time()
        context['next_date'] = (_date + timedelta(weeks=1)).strftime("%Y-%m-%d")
        context['prev_date'] = (_date - timedelta(weeks=1)).strftime("%Y-%m-%d")
        return context






