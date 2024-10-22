from datetime import datetime
import pickle

from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.core.cache import cache

from booking.views import CampusListView, AudienceListView, AudienceDetailView
from booking.models import Campus, Audience, User, Reservation



class CampusViewTests(TestCase):
    def setUp(self):
        self.campus = Campus.objects.create(
            title='test',
            address='-',
            phone='-',
            start_of_work=timezone.datetime(2024, 12, 1, 8, 0),
            end_of_work=timezone.datetime(2024, 12, 1, 20, 0),
            is_active=True
        )
        self.view = CampusListView()

    def test_query_set(self):
        self.assertIsNone(cache.get('campuses'))

        self.assertQuerySetEqual(
            self.view.get_queryset(), Campus.objects.all()
        )

        self.assertIsNotNone(cache.get('campuses'))
        self.assertQuerySetEqual(
            pickle.loads(cache.get('campuses')), Campus.objects.all()
        )

class AudienceViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.campus = Campus.objects.create(
            title='test',
            address='-',
            phone='-',
            start_of_work=timezone.datetime(2024, 12, 1, 8, 0),
            end_of_work=timezone.datetime(2024, 12, 1, 20, 0),
            is_active=True
        )
        self.user = User.objects.create_user('test_user')
        self.audience = Audience.objects.create(
            campus=self.campus,
            user=self.user,
            floor=1,
            title=111
        )
        self.view = AudienceListView()

    def test_query_set(self):
        kwargs = {
            'campus': self.campus.id
        }
        request = self.factory.get(reverse('audience_list_view', kwargs=kwargs))
        self.view.setup(request, **kwargs)

        self.assertIsNone(cache.get(f'campus_audiences:{self.campus.id}'))
        self.assertQuerySetEqual(
            self.view.get_queryset(), Audience.objects.filter(campus=self.campus)
        )
        self.assertIsNotNone(cache.get(f'campus_audiences:{self.campus.id}'))

        self.assertQuerySetEqual(
            pickle.loads(cache.get(f'campus_audiences:{self.campus.id}')),
            Audience.objects.filter(campus__id=self.campus.id)
        )

    def test_context_data(self):
        client = Client()

        self.assertIsNone(cache.get(f'floors:{self.campus.id}'))
        response = client.get(reverse('audience_list_view', kwargs={'campus' : self.campus.id}))
        self.assertIsNotNone(cache.get(f'floors:{self.campus.id}'))

        floor = self.audience.floor
        self.assertQuerySetEqual(
            response.context['floors'], [floor]
        )
        self.assertQuerySetEqual(
            response.context['audiences'], [self.audience]
        )



class AudienceDetailViewTest(TestCase):
    def setUp(self):
        self.campus = Campus.objects.create(
            title='test',
            address='-',
            phone='-',
            start_of_work=timezone.datetime(2024, 12, 1, 8, 0),
            end_of_work=timezone.datetime(2024, 12, 1, 20, 0),
            is_active=True
        )
        self.user = User.objects.create_user('test_user')
        self.audience = Audience.objects.create(
            campus=self.campus,
            user=self.user,
            floor=1,
            title=111
        )
        self.view = AudienceDetailView()
        self.factory = RequestFactory()


    def test_form_kwargs(self):
        kwargs = dict(campus=self.campus.id, audience_id=self.audience.id)
        request = self.factory.get(
            reverse(
                'audience_detail',
                kwargs=kwargs
            )
        )
        self.view.setup(request, **kwargs)
        data = self.view.get_form_kwargs()
        self.assertTrue(
            'audience' in data
        )

    def test_object(self):
        kwargs = dict(campus=self.campus.id, audience_id=self.audience.id)
        request = self.factory.get(
            reverse(
                'audience_detail',
                kwargs=kwargs
            )
        )
        self.view.setup(request, **kwargs)

        self.assertIsNone(cache.get(f'audience:{self.audience.id}'))
        obj = self.view.get_object()
        self.assertIsNotNone(cache.get(f'audience:{self.audience.id}'))

        self.assertEqual(
            obj, Audience.objects.get(pk=self.audience.id)
        )

    def test_context_data(self):
        reservation = Reservation(
            audience=self.audience,
            title='134',
            time_start=datetime(2025, 10, 25, 8, 45),
            time_end=datetime(2025, 10, 25, 10, 20),
            speaker='Lector',
            type='seminar'
        )
        reservation.save()

        kwargs = dict(campus=self.campus.id, audience_id=self.audience.id)
        request = self.factory.get(
            reverse(
                'audience_detail',
                kwargs=kwargs
            )
        )
        self.view.setup(request, **kwargs)

        self.assertIsNone(cache.get(f'audience_reservations:{self.audience.id}'))
        context = self.view.get_context_data(**kwargs)
        self.assertIsNotNone(cache.get(f'audience_reservations:{self.audience.id}'))

        self.assertTrue('reservations' in context)
        self.assertTrue('form' in context)
        self.assertTrue('date' in context)
        self.assertTrue('days' in context)
        self.assertTrue('class_time' in context)
        self.assertTrue('next_date' in context)
        self.assertTrue('prev_date' in context)

        self.assertQuerySetEqual(
            context['reservations'], [reservation]
        )



