from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.utils import timezone
from django.views.generic import ListView

from booking.views import CampusListView, AudienceListView
from booking.models import Campus, Audience, User


class CampusViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.campus = Campus.objects.create(
            title='test',
            address='-',
            phone='-',
            start_of_work=timezone.datetime(2024, 12, 1, 8, 0),
            end_of_work=timezone.datetime(2024, 12, 1, 20, 0)
        )
        self.view = CampusListView()

    def test_query_set(self):
        self.assertQuerySetEqual(
            self.view.queryset, [self.campus]
        )

class AudienceViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.campus = Campus.objects.create(
            title='test',
            address='-',
            phone='-',
            start_of_work=timezone.datetime(2024, 12, 1, 8, 0),
            end_of_work=timezone.datetime(2024, 12, 1, 20, 0)
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
        self.assertQuerySetEqual(
            self.view.get_queryset(), [self.audience]
        )

    def test_context_data(self):
        client = Client()
        response = client.get(reverse('audience_list_view', kwargs={'campus' : self.campus.id}))
        floor = self.audience.floor
        self.assertQuerySetEqual(
            response.context['floors'], [floor]
        )
        self.assertQuerySetEqual(
            response.context['audiences'], [self.audience]
        )






