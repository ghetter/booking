from django import forms
from booking.models import Reservation


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ('title', 'time_start', 'time_end')

    def __init__(self, *args, **kwargs):
        self.audience = kwargs.pop('audience', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.audience:
            instance.audience = self.audience
        if commit: instance.save()
        return instance
