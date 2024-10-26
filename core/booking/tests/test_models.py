from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.test import TestCase
from datetime import datetime, timezone

from booking.models import Campus, Reservation, Audience, User

def create_campus_object(title):
    return Campus.objects.create(
        title=title,
        phone='-',
        address='-',
        start_of_work=datetime(2024, 12, 1, 8, 0, tzinfo=timezone.utc),
        end_of_work=datetime(2024, 12, 1, 20, 0, tzinfo=timezone.utc),
        is_active=True
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

    def test_time_of_work(self):
        day_start = self.campus1.start_of_work.date().strftime('%A')
        day_end = self.campus1.end_of_work.date().strftime('%A')
        time_start = self.campus1.start_of_work.time().strftime('%H:%M')
        time_end = self.campus1.end_of_work.time().strftime('%H:%M')
        self.assertEqual(
            self.campus1.get_time_of_work(), f"{day_start}-{day_end}: {time_start}-{time_end}"
        )



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
            type='lecture'
        )
        self.reservation2 = Reservation.objects.create(
            audience=self.audience2,
            title='R2',
            time_start=datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc),
            speaker='lector',
            type='lecture'
        )

    def test_datetime(self):
        self.assertEqual(self.reservation1.time_start, datetime(2024, 10, 1, 10, 30, tzinfo=timezone.utc))
        self.assertEqual(self.reservation2.time_start, datetime(2024, 10, 1, 14, 30, tzinfo=timezone.utc))

        self.assertEqual(self.reservation1.time_end, datetime(2024, 10, 1, 12, 30, tzinfo=timezone.utc))
        self.assertEqual(self.reservation2.time_end, datetime(2024, 10, 1, 18, 30, tzinfo=timezone.utc))

    def test_time_interval(self):
        campus = Campus(
            title='test_time',
            address='-',
            phone='-',
            start_of_work=datetime(2024, 1, 12, 8, 0, tzinfo=timezone.utc),
            end_of_work=datetime(2024, 1, 12, 20, 0, tzinfo=timezone.utc),
            is_active=True
        )
        audience = Audience(
            campus=campus,
            user=self.user1,
            title=12,
            floor=12
        )
        bad_reservation = Reservation(
            audience=audience,
            title='R3',
            time_start=datetime(2024, 10, 1, 1, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 4, 30, tzinfo=timezone.utc),
            speaker='lector',
            type='lecture'
        )
        exception_message = "Fail. Hours of reservation between %d and %d not allowed." % (campus.end_of_work.hour, campus.start_of_work.hour)
        with self.assertRaisesMessage(ValidationError, exception_message):
            bad_reservation.validate_time_interval()

        good_reservation = Reservation(
            audience=audience,
            title='R3',
            time_start=datetime(2024, 10, 1, 8, 0, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 16, 0, tzinfo=timezone.utc),
            speaker='lector',
            type='lecture'
        )
        self.assertIsNone(good_reservation.validate_time_interval())



    def test_exist_reservation(self):
        with self.assertRaisesMessage(ValidationError, 'Fail. In that time audience is reserved.'):
            exist_reservation = Reservation(
                audience=self.audience2,
                title='R_EXIST',
                time_start=datetime(2024, 10, 1, 15, 30, tzinfo=timezone.utc),
                time_end=datetime(2024, 10, 1, 16, 30, tzinfo=timezone.utc),
                speaker='lector',
                type='lecture'
            )
            exist_reservation.check_exist_reservation()


        no_exist_reservation = Reservation(
            audience=self.audience2,
            title='R_NO_EXIST',
            time_start=datetime(2024, 10, 1, 7, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 9, 30, tzinfo=timezone.utc),
            speaker='lector',
            type='lecture'
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
                type='lecture'
            )
            invalid_reservation.check_range_of_date()

        valid_reservation = Reservation(
            audience=self.audience2,
            title='Valid range',
            time_start=datetime(2024, 10, 17, 7, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 17, 9, 30, tzinfo=timezone.utc),
            speaker='lector',
            type='lecture'
        )
        valid_reservation.check_range_of_date()

    def test_update_type_in_model(self):
        reservation = Reservation(
            audience=self.audience2,
            title='some reservation',
            time_start=datetime(2024, 10, 17, 8, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 17, 9, 30, tzinfo=timezone.utc),
            speaker='lector',
            type='lecture'
        )
        reservation.save()

        reservation.type = 'examination'
        self.assertIsNone(reservation.check_exist_reservation())




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


class CacheTest(TestCase):
    def setUp(self):
        self.campus = Campus(
            title='some_campus',
            phone='-',
            address='-',
            start_of_work=datetime(2024, 12, 1, 8, 0, tzinfo=timezone.utc),
            end_of_work=datetime(2024, 12, 1, 20, 0, tzinfo=timezone.utc),
            is_active=True
        )
        self.campus.save()
        self.user = User.objects.create_user('test_user')
        self.audience = Audience(
            campus=self.campus,
            user=self.user,
            title=1,
            floor=1
        )
        self.audience.save()
        self.reservation = Reservation(
            audience=self.audience,
            title='R3',
            time_start=datetime(2024, 10, 1, 8, 30, tzinfo=timezone.utc),
            time_end=datetime(2024, 10, 1, 19, 30, tzinfo=timezone.utc),
            speaker='lector',
            type='lecture'
        )
        self.reservation.save()
        self.keys = [
            'campuses',
            f'campus_audiences:{self.campus.id}',
            f'floors:{self.campus.id}',
            f'audience:{self.audience.id}',
            f'audience_reservations:{self.audience.id}',
        ]

    def test_cache(self):
        self.assertEqual(
            cache.get_many(self.keys), {}
        )


