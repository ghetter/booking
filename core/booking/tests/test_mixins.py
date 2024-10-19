from datetime import datetime, date, time, timedelta

from django.test import TestCase, RequestFactory
from django.urls import reverse



from booking.mixins import LessonMixin

class LessonMixinTest(TestCase):
    def setUp(self):
        self.mixin = LessonMixin()
        self._date = date(2024, 10, 14)
        self.factory = RequestFactory()

    def test_range_of_the_week(self):
        start_week, end_week = self.mixin.get_the_range_of_the_week(self._date)

        self.assertEqual(
            start_week, date(2024, 10, 14)
        )
        self.assertEqual(
            end_week, date(2024, 10, 19)
        )

    def test_date_from_params(self):
        kwargs = dict(
            campus=1,
            audience_id=1
        )
        request_without_params = self.factory.get(
            reverse('audience_detail', kwargs=kwargs),
        )
        self.assertEqual(
            self.mixin.get_date_from_query_params(request_without_params),
            date.today()
        )

        request_with_params = self.factory.get(
            reverse('audience_detail', kwargs=kwargs),
            query_params={
                'date' : '2024-10-14'
            }
        )
        self.assertEqual(
            self.mixin.get_date_from_query_params(request_with_params),
            self._date
        )

    def test_days(self):
        days_from_mixin = self.mixin.get_days(self._date)
        days = [
            date(2024, 10, i) for i in range(14, 20)
        ]
        self.assertEqual(
            days_from_mixin, days
        )

