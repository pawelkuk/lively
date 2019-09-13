from django.contrib import admin

from measurement.models import MeasurementType, Measurement
admin.site.register(Measurement)
admin.site.register(MeasurementType)
