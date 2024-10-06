from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import datetime, timezone

from booking.models import Campus, Reservation, Audience, User

def create_campus_object(title):
    return Campus.objects.create(
        title=title,
        phone='-',
        address='-',
        start_of_work=datetime.now(tz=timezone.utc),
        end_of_work=datetime.now(tz=timezone.utc)
    )

class CampusTestCase(TestCase):
    def setUp(self):
        self.campus1 = create_campus_object('Num 1')
        self.campus2 = create_campus_object('Num 2')

    def test_title(self):
        self.assertEqual(self.campus1.title, 'Num 1')
        self.assertEqual(self.campus2.title, 'Num 2')

    def test_magic_str_method(self):
        self.assertEqual(self.campus1.__str__(), 'Num 1')
        self.assertEqual(self.campus2.__str__(), 'Num 2')

    def test_meta_class(self):
        self.assertEqual(self.campus1._meta.verbose_name_plural, 'Корпуса')
        self.assertEqual(self.campus2._meta.verbose_name_plural, 'Корпуса')

class ReservationTestCase(TestCase):
    def setUp(self):
        self.campus1 = create_campus_object("test_campus_1")
        self.campus2 = create_campus_object("test_campus_2")
        self.user1 = User.objects.create_user('test_user_1')
        self.user2 = User.objects.create_user('test_user_2')
        self.audience1 = Audience.objects.create(
            campus=self.campus1,
            user=self.user1,
            title=1,
            floor=1
        )
        self.audience2 = Audience.objects.create(
            campus=self.campus2,
            user=self.user2,
            title=2,
            floor=1
        )
        self.reservation1 = Reservation.objects.create(
            audience=self.audience1,
            title='R1',
            time_start=datetime(2024, 10, 1, 10, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 12, 30, tzinfo=timezone.utc),
            speaker='lector',
            _type='lecture'
        )
        self.reservation2 = Reservation.objects.create(
            audience=self.audience2,
            title='R2',
            time_start=datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc),
            speaker='lector',
            _type='lecture'
        )

    def test_datetime(self):
        self.assertEqual(self.reservation1.time_start, datetime(2024, 10, 1, 10, 30, tzinfo=timezone.utc))
        self.assertEqual(self.reservation2.time_start, datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc))

        self.assertEqual(self.reservation1.time_end, datetime(2024, 10, 1, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(self.reservation2.time_end, datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc))

    def test_time_interval(self):
        self.assertIsNone(self.reservation1.validate_time_interval())
        self.assertIsNone(self.reservation2.validate_time_interval())


    def test_exist_reservation(self):
        with self.assertRaisesMessage(ValidationError, 'Fail. In that time audience is reserved.'):
            exist_reservation = Reservation(
                audience=self.audience2,
                title='R_EXIST',
                time_start=datetime(2024, 10, 1, 15, 30, tzinfo=timezone.utc),
                time_end=datetime(2024, 10, 1, 16, 30, tzinfo=timezone.utc),
                speaker='lector',
                _type='lecture'
            )
            exist_reservation.check_exist_reservation()


        no_exist_reservation = Reservation(
            audience=self.audience2,
            title='R_NO_EXIST',
            time_start=datetime(2024, 10, 1, 7, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 9, 30, tzinfo=timezone.utc),
            speaker='lector',
            _type='lecture'
        )
        no_exist_reservation.check_exist_reservation()

    def test_range_of_date(self):
        with self.assertRaisesMessage(ValidationError, 'Fail. Check range of date.'):
            invalid_reservation = Reservation(
                audience=self.audience2,
                title='Invalid range',
                time_start=datetime(2024, 10, 17, 7, 30, tzinfo=timezone.utc),
                time_end=datetime(2024, 10, 1, 9, 30, tzinfo=timezone.utc),
                speaker='lector',
                _type='lecture'
            )
            invalid_reservation.check_range_of_date()

        valid_reservation = Reservation(
            audience=self.audience2,
            title='Valid range',
            time_start=datetime(2024, 10, 17, 7, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 17, 9, 30, tzinfo=timezone.utc),
            speaker='lector',
            _type='lecture'
        )
        valid_reservation.check_range_of_date()



class AudienceTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user('test_user_1')
        user2 = User.objects.create_user('test_user_2')
        campus1 = create_campus_object('test_campus_1')
        campus2 = create_campus_object('test_campus_2')

        self.aud1 = Audience.objects.create(
            campus=campus1,
            user=user1,
            title=1,
            floor=1
        )
        self.aud2 = Audience.objects.create(
            campus=campus2,
            user=user2,
            title=2,
            floor=2
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

