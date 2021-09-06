import os
from PIL import Image

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage as storage
from django.forms import ModelForm, TextInput, RadioSelect, HiddenInput, FloatField, NumberInput, Select, IntegerField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.contrib.sites.models import Site


from . import models


class ReservationForm(ModelForm):

    def __init__(self, free_seats, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['pax'] = IntegerField(widget=Select(choices=[tuple([x,x]) for x in range(1, free_seats + 1)]))

    class Meta:
        model = models.Reservation
        fields = [
            'pax',
            'name',
            'email',
            'mobile',
            'comments',
            'reservation_code',
        ]

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("reservation_code")
        current_site = Site.objects.get_current()

        if code != current_site.siteproperty.reservation_code:
            msg = _("You need to enter a valid code. You can find this code on flyers or social networks or by contacting the host.")
            self.add_error('reservation_code', msg)
