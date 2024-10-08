from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Campus(models.Model):
    title = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    start_of_work = models.DateTimeField()
    end_of_work = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Корпуса'
        verbose_name = 'Корпус'

    def get_time_of_work(self):
        day_start = self.start_of_work.date().strftime('%A')
        day_end = self.end_of_work.date().strftime('%A')
        time_start = self.start_of_work.time().strftime('%H:%M')
        time_end = self.end_of_work.time().strftime('%H:%M')
        return f"{day_start}-{day_end}: {time_start}-{time_end}"

    def __str__(self):
        return self.title

class Audience(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='audiences')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audiences')
    title = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'Аудитории'
        verbose_name = 'Аудитория'

    def __str__(self):
        return self.title

class Reservation(models.Model):
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name='reservations')
    title = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    speaker = models.CharField(max_length=70)
    _type = models.CharField(
        max_length=20,
        choices={
            'lecture' : 'Лекция',
            'seminar': 'Семинар',
            'examination': 'Экзамен',
        },
        default='Лекция'
    )

    class Meta:
        verbose_name_plural = 'Забронированные аудитории'
        verbose_name = 'Забронированная аудитория'

    def __str__(self):
        return self.title

    def validate_time_interval(self):
        h_start = self.time_start.hour
        h_end = self.time_end.hour
        hour_start_campus = self.audience.campus.start_of_work.hour
        hour_end_campus = self.audience.campus.end_of_work.hour
        if h_end < hour_start_campus or h_start < hour_start_campus:
            raise ValidationError('Fail. Hours of reservation between %d and %d not allowed.' % (hour_end_campus, hour_start_campus))
        if h_end >= hour_end_campus or h_start >= hour_end_campus:
            raise ValidationError('Fail. Hours of reservation between %d and %d not allowed.' % (hour_end_campus, hour_start_campus))

    def check_range_of_date(self):
        if self.time_end < self.time_start:
            raise ValidationError('Fail. Check range of date.')

    def check_exist_reservation(self):
        objects = Reservation.objects.filter(time_start__date=self.time_start.date())
        for object in objects:
            if (object.time_start <= self.time_start <= object.time_end) or (object.time_start <= self.time_end <= object.time_end):
                raise ValidationError('Fail. In that time audience is reserved.')

    def save(self, *args, **kwargs):
        self.check_range_of_date()
        self.validate_time_interval()
        self.check_exist_reservation()
        return super().save(*args, **kwargs)
