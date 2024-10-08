from django.test import TestCase
from django.urls import reverse, resolve

from booking.views import CampusListView, AudienceListView

class UrlsTestCase(TestCase):
    def test_audiences_url(self):
        name = 'audience_list_view'
        path = reverse(name, kwargs={'campus' : 1})
        self.assertEqual(
            resolve(path).func.view_class, AudienceListView
        )

    def test_campus_url(self):
        name = 'campus_list_view'
        path = reverse(name)
        self.assertEqual(
            resolve(path).func.view_class, CampusListView
        )