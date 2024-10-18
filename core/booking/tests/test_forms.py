from django.test import TestCase
from django.utils import timezone

from booking.models import Campus, User, Audience
from booking.forms import ReservationForm

class ReservationFormTest(TestCase):
    def test_init(self):
        form = ReservationForm()
        self.assertIsNone(form.audience)

        campus = Campus.objects.create(
            title='test',
            address='-',
            phone='-',
            start_of_work=timezone.datetime(2024, 12, 1, 8, 0),
            end_of_work=timezone.datetime(2024, 12, 1, 20, 0),
            is_active=True
        )
        user = User.objects.create_user('test_user')
        audience = Audience.objects.create(
            campus=campus,
            user=user,
            floor=1,
            title=111
        )
        form = ReservationForm(audience=audience)
        self.assertIsNotNone(form.audience)
