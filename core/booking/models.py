from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Campus(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    class Meta:
        verbose_name_plural = 'Корпуса'
        verbose_name = 'Корпус'

    def __str__(self):
        return self.title


class Audience(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='audiences')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audiences')
    title = models.PositiveSmallIntegerField()

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

    class Meta:
        verbose_name_plural = 'Забронированные аудитории'
        verbose_name = 'Забронированная аудитория'

    def __str__(self):
        return self.title

    def validate_time_interval(self):
        h_start = self.time_start.hour
        h_end = self.time_end.hour
        if 0 <= h_start < 6 or 0 <= h_end < 6:
            raise ValidationError('Fail. Hours of reservation between 0 and 6 not allowed.')

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
