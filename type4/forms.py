from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

class ChangesForm(forms.Form):
    from_timestamp = forms.DateTimeField()
    to_timestamp = forms.DateTimeField()