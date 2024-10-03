from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Campus, Reservation, Audience, User
from datetime import datetime, date, timedelta, timezone, time

class CampusTestCase(TestCase):
    def setUp(self):
        Campus.objects.create(title='Num 2')
        Campus.objects.create(title='Num 1')

    def test_title(self):
        f = Campus.objects.get(title="Num 1")
        s = Campus.objects.get(title="Num 2")
        self.assertEqual(f.title, 'Num 1')
        self.assertEqual(s.title, 'Num 2')


    def test_magic_str_method(self):
        f = Campus.objects.get(title="Num 1")
        s = Campus.objects.get(title="Num 2")
        self.assertEqual(f.__str__(), 'Num 1')
        self.assertEqual(s.__str__(), 'Num 2')

    def test_meta_class(self):
        f = Campus.objects.get(title="Num 1")
        s = Campus.objects.get(title="Num 2")
        self.assertEqual(f._meta.verbose_name_plural, 'campuses')
        self.assertEqual(s._meta.verbose_name_plural, 'campuses')

class ReservationTestCase(TestCase):
    def setUp(self):
        self.campus1 = Campus.objects.create(title="test_campus_1")
        self.campus2 = Campus.objects.create(title="test_campus_2")
        self.user1 = User.objects.create_user('test_user_1')
        self.user2 = User.objects.create_user('test_user_2')
        self.audience1 = Audience.objects.create(
            campus=self.campus1,
            user=self.user1,
            title=1
        )
        self.audience2 = Audience.objects.create(
            campus=self.campus2,
            user=self.user2,
            title=2
        )
        Reservation.objects.create(
            audience=self.audience1,
            title='R1',
            time_start=datetime(2024, 10, 1, 10, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 12, 30, tzinfo=timezone.utc),
            date=date.today()
        )
        Reservation.objects.create(
            audience=self.audience2,
            title='R2',
            time_start=datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc),
            date=date.today()
        )

    def test_date(self):
        r1 = Reservation.objects.get(title='R1')
        r2 = Reservation.objects.get(title='R2')

        self.assertEqual(r1.date, date.today())
        self.assertEqual(r2.date, date.today())

    def test_datetime(self):
        r1 = Reservation.objects.get(title='R1')
        r2 = Reservation.objects.get(title='R2')

        self.assertEqual(r1.time_start, datetime(2024, 10, 1, 10, 30, tzinfo=timezone.utc))
        self.assertEqual(r2.time_start, datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc))

        self.assertEqual(r1.time_end, datetime(2024, 10, 1, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(r2.time_end, datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc))

    def test_time_interval(self):
        r1 = Reservation.objects.get(title='R1')
        r2 = Reservation.objects.get(title='R2')
        self.assertEqual(r1.validate_time_interval(), True)
        self.assertEqual(r2.validate_time_interval(), True)

    def test_exist_reservation(self):
        r1 = Reservation(
            audience=self.audience1,
            title="окружающий мир",
            time_start=datetime(2024, 10, 3, 17, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 3, 19, 0, tzinfo=timezone.utc),
            date=date(2024, 10, 3)
        )
        r1.save()
        r2 = Reservation(
            audience=self.audience1,
            title="окружающий мир",
            time_start=datetime(2024, 10, 3, 18, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 3, 23, 0, tzinfo=timezone.utc),
            date=date(2024, 10, 3)
        )
        with self.assertRaisesMessage(ValidationError, 'busy'):
            r2.save()
        r3 = Reservation(
            audience=self.audience1,
            title="окружающий мир",
            time_start=datetime(2024, 10, 3, 15, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 3, 18, 25, tzinfo=timezone.utc),
            date=date(2024, 10, 3)
        )
        with self.assertRaisesMessage(ValidationError, 'busy'):
            r3.save()





class AudienceTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('test_user_1')
        user2 = User.objects.create_user('test_user_2')
        campus1 = Campus.objects.create(title='test_campus_1')
        campus2 = Campus.objects.create(title='test_campus_2')

        Audience.objects.create(
            campus=campus1,
            user=user1,
            title=1
        )
        Audience.objects.create(
            campus=campus2,
            user=user2,
            title=2
        )

    def test_campuses(self):
        aud1 = Audience.objects.get(title=1)
        aud2 = Audience.objects.get(title=2)

        self.assertEqual(aud1.campus, Campus.objects.get(title='test_campus_1'))
        self.assertEqual(aud2.campus, Campus.objects.get(title='test_campus_2'))

    def test_users(self):
        aud1 = Audience.objects.get(title=1)
        aud2 = Audience.objects.get(title=2)

        self.assertEqual(aud1.user, User.objects.get_by_natural_key('test_user_1'))
        self.assertEqual(aud2.user, User.objects.get_by_natural_key('test_user_2'))

    def test_meta(self):
        aud1 = Audience.objects.get(title=1)
        aud2 = Audience.objects.get(title=2)

        self.assertEqual(aud1._meta.verbose_name_plural, 'audiences')
        self.assertEqual(aud2._meta.verbose_name_plural, 'audiences')

