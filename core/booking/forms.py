from datetime import time, date, datetime
from django import forms
from django.core.cache import cache
from booking.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('title', 'speaker', 'time_end', 'time_start', 'type')

    def __init__(self, *args, **kwargs):
        self.audience = kwargs.pop('audience', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        cache.clear()
        instance = super().save(commit=False)
        if self.audience:
            instance.audience = self.audience
        if commit: instance.save()
        return instance
