from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Campus, Reservation, Audience, User
from datetime import datetime, timezone

class CampusTestCase(TestCase):
    def setUp(self):
        self.c1 = Campus.objects.create(title='Num 1')
        self.c2 = Campus.objects.create(title='Num 2')

    def test_title(self):
        self.assertEqual(self.c1.title, 'Num 1')
        self.assertEqual(self.c2.title, 'Num 2')


    def test_magic_str_method(self):
        self.assertEqual(self.c1.__str__(), 'Num 1')
        self.assertEqual(self.c2.__str__(), 'Num 2')

    def test_meta_class(self):
        self.assertEqual(self.c1._meta.verbose_name_plural, 'Корпуса')
        self.assertEqual(self.c2._meta.verbose_name_plural, 'Корпуса')

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
        self.r1 = Reservation.objects.create(
            audience=self.audience1,
            title='R1',
            time_start=datetime(2024, 10, 1, 10, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 12, 30, tzinfo=timezone.utc),
        )
        self.r2 = Reservation.objects.create(
            audience=self.audience2,
            title='R2',
            time_start=datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc),
        )

    def test_datetime(self):
        self.assertEqual(self.r1.time_start, datetime(2024, 10, 1, 10, 30, tzinfo=timezone.utc))
        self.assertEqual(self.r2.time_start, datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc))

        self.assertEqual(self.r1.time_end, datetime(2024, 10, 1, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(self.r2.time_end, datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc))

    def test_time_interval(self):
        self.assertIsNone(self.r1.validate_time_interval())
        self.assertIsNone(self.r2.validate_time_interval())


    def test_exist_reservation(self):
        with self.assertRaisesMessage(ValidationError, 'В данное время аудитория занята.'):
            Reservation.objects.create(
                audience=self.audience2,
                title='R_EXIST',
                time_start=datetime(2024, 10, 1, 15, 30, tzinfo=timezone.utc),
                time_end=datetime(2024, 10, 1, 16, 30, tzinfo=timezone.utc),
            )


        Reservation.objects.create(
            audience=self.audience2,
            title='R_NO_EXIST',
            time_start=datetime(2024, 10, 1, 7, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 9, 30, tzinfo=timezone.utc),
        )

    def test_range_of_date(self):
        with self.assertRaisesMessage(ValidationError, 'Указанный интервал бронирования невозможен. Бронь кончается раньше, чем начинается.'):
            Reservation.objects.create(
                audience=self.audience2,
                title='Invalid range',
                time_start=datetime(2024, 10, 17, 7, 30, tzinfo=timezone.utc),
                time_end=datetime(2024, 10, 1, 9, 30, tzinfo=timezone.utc),
            )

        Reservation.objects.create(
            audience=self.audience2,
            title='Valid range',
            time_start=datetime(2024, 10, 17, 7, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 17, 9, 30, tzinfo=timezone.utc),
        )



class AudienceTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('test_user_1')
        user2 = User.objects.create_user('test_user_2')
        campus1 = Campus.objects.create(title='test_campus_1')
        campus2 = Campus.objects.create(title='test_campus_2')

        self.aud1 = Audience.objects.create(
            campus=campus1,
            user=user1,
            title=1
        )
        self.aud2 = Audience.objects.create(
            campus=campus2,
            user=user2,
            title=2
        )

    def test_campuses(self):
        self.assertEqual(self.aud1.campus, Campus.objects.get(title='test_campus_1'))
        self.assertEqual(self.aud2.campus, Campus.objects.get(title='test_campus_2'))

    def test_users(self):
        self.assertEqual(self.aud1.user, User.objects.get_by_natural_key('test_user_1'))
        self.assertEqual(self.aud2.user, User.objects.get_by_natural_key('test_user_2'))

    def test_meta(self):
        self.assertEqual(self.aud1._meta.verbose_name_plural, 'Аудитории')
        self.assertEqual(self.aud2._meta.verbose_name_plural, 'Аудитории')

