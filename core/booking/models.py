from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Campus(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    class Meta:
        verbose_name_plural = 'campuses'

    def __str__(self):
        return self.title

    # TODO добавить поле title(название корпуса), настроить Meta class


class Audience(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='audiences')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audiences')
    title = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'audiences'

    def __str__(self):
        return self.title

    # TODO добавить поле title(номер аудитории), настроить Meta class

class Reservation(models.Model):
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name='reservations')
    title = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    date = models.DateField()

    class Meta:
        verbose_name_plural = 'reservations'

    def __str__(self):
        return self.title

    def validate_time_interval(self):
        h_start = self.time_start.hour
        h_end = self.time_end.hour
        if 0 <= h_start < 6 or 0 <= h_end < 6:
            return False
        return True


    def check_exist_reservation(self):
        objects = Reservation.objects.all()
        for object in objects:
            if object.time_start <= self.time_start <= object.time_end:
                raise ValidationError('busy')
            if object.time_start <= self.time_end <= object.time_end:
                raise ValidationError('busy')


    def save(self, *args, **kwargs):
        self.check_exist_reservation()
        return super().save(*args, **kwargs)

    # TODO добавить поля title(название урока), time_start, time_end, настроить Meta class
    #  прописать Validators таким образом, чтобы нельзя было бронировать аудитории на ночь (с 00:00 до 06:00)
    #  сделать так, что бы нельзя было забронировать одну аудиторию на одно и то-же время два раза и более (method save)
