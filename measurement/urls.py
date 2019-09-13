from django.conf.urls import url
from .views import measurement_form, measurement_type_form, measurement_csv_form

urlpatterns = [
    url('^measurementform/',
        measurement_form,
        name='measurement_form'),
    url('^measurementtypeform/',
        measurement_type_form,
        name='measurement_type_form'),
    url('^measurementcsvform/',
        measurement_csv_form,
        name='measurement_csv_form'),
]
