from django.contrib.auth.models import User
from django.db import models


class Campus(models.Model):
    title = None

    class Meta:
        pass

    def __str__(self):
        return self.title

    # TODO добавить поле title(название корпуса), настроить Meta class


class Audience(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='audiences')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audiences')
    title = None

    class Meta:
        pass

    def __str__(self):
        return self.title

    # TODO добавить поле title(номер аудитории), настроить Meta class


class Reservation(models.Model):
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name='reservations')
    title = None
    time_start = None
    time_end = None

    class Meta:
        pass

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    # TODO добавить поля title(название урока), time_start, time_end, настроить Meta class
    #  прописать Validators таким образом, чтобы нельзя было бронировать аудитории на ночь (с 00:00 до 06:00)
    #  сделать так, что бы нельзя было забронировать одну аудиторию на одно и то-же время два раза и более (method save)
