from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from booking.views import CampusListView, AudienceListView
from booking.models import Campus

class CampusViewTests(TestCase):
    @staticmethod
    def create_campus_object(**kwargs):
        d = {
            'title' : 'test',
            'phone' : 'test',
            'address' : 'test',
            'start_of_work' : timezone.now(),
            'end_of_work' : timezone.now()
        }
        d.update(kwargs)
        return Campus.objects.create(**d)

    def test_status_code(self):
        response = self.client.get(reverse('campus_list_view'))
        self.assertEqual(response.status_code, 200)

    def test_equal_query_set(self):
        campus = self.create_campus_object()
        response = self.client.get(reverse('campus_list_view'))
        self.assertQuerySetEqual(
            response.context['campuses'], [campus]
        )

    def test_response_content(self):
        self.create_campus_object()
        response = self.client.get(reverse('campus_list_view'))
        self.assertContains(response, "Телефон")

    def test_response_without_objects(self):
        response = self.client.get(reverse('campus_list_view'))
        self.assertContains(response, 'Нет кампусов')

    def test_more_content(self):
        self.create_campus_object()
        self.create_campus_object(title='test2')
        response = self.client.get(reverse('campus_list_view'))
        self.assertContains(response, 'Телефон', count=2)

