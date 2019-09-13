from measurement.models import Measurement, MeasurementType
from django.forms import ModelForm
from django import forms


class CsvForm(forms.Form):
    file = forms.FileField(label='File')


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ['measurement_type', 'measurement', 'units', 'note']


class MeasurementTypeForm(ModelForm):
    class Meta:
        model = MeasurementType
        fields = ['name']


class MeasurementProgressForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ['measurement_type']

