import json
import pickle

from datetime import datetime, timedelta, date, time

from django.urls import reverse_lazy
from django.core.cache import cache
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

    def get_queryset(self):
        campuses = cache.get('campuses')
        if campuses is None:
            campuses = Campus.objects.all()
            cache.set('campuses', pickle.dumps(campuses), 60 * 10)
        else:
            campuses = pickle.loads(campuses)
        return campuses

    # TODO: прописать отображение кампуса к url главной страницы,
    #  отобразить информацию для Frontend


class AudienceListView(ListView):
    model = Audience
    template_name = 'booking/main_func/audience_list.html'
    context_object_name = 'audiences'

    def get_queryset(self):
        campus_id = self.kwargs['campus']
        campus = cache.get(f'campus:{campus_id}')

        if campus is None:
            campus = Campus.objects.get(id=campus_id)
            cache.set(f'campus:{campus_id}', pickle.dumps(campus), 60 * 10)
        else:
            campus = pickle.loads(campus)

        audiences = cache.get(f'campus_audiences:{campus_id}')
        if audiences is None:
            audiences = Audience.objects.filter(campus=campus)
            cache.set(f'campus_audiences:{campus_id}', pickle.dumps(audiences), 60 * 10)
        else:
            audiences = pickle.loads(audiences)

        return audiences

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campus_id = self.kwargs['campus']
        floors = cache.get(f'floors:{campus_id}')
        if floors is None:
            floors = self.object_list.values_list('floor', flat=True).order_by().distinct()
            cache.set(f'floors:{campus_id}', pickle.dumps(floors), 60 * 10)
        else:
            floors = pickle.loads(floors)
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
        audience_id = self.kwargs[self.pk_url_kwarg]
        audience = cache.get(f'audience:{audience_id}')
        if audience is None:
            audience = Audience.objects.get(pk=audience_id)
            cache.set(f'audience:{audience_id}', pickle.dumps(audience), 60 * 10)
        else:
            audience = pickle.loads(audience)
        return audience

        # TODO: Дописать query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        audience_id = self.object.id
        _date = self.get_date_from_query_params(self.request)
        reservations = cache.get(f'audience_reservations:{audience_id}')
        if reservations is None:
            reservations = self.object.reservations.filter(
                time_start__week=_date.isocalendar().week,
                time_end__week=_date.isocalendar().week
            )
            cache.set(f'audience_reservations:{audience_id}', pickle.dumps(reservations), 60 * 10)
        else:
            reservations = pickle.loads(reservations)
        context['reservations'] = reservations
        context['form'] = self.get_form()

        context['date'] = self.get_the_range_of_the_week_str(_date)
        context['days'] = self.get_days(_date)
        context['class_time'] = self.get_class_time()
        context['next_date'] = (_date + timedelta(weeks=1)).strftime("%Y-%m-%d")
        context['prev_date'] = (_date - timedelta(weeks=1)).strftime("%Y-%m-%d")
        return context






