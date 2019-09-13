from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from measurement.forms import MeasurementForm, MeasurementTypeForm, CsvForm
from measurement.models import Measurement, MeasurementType
from user.views import home

import csv
import io
from datetime import datetime

@login_required
def measurement_form(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            return home(request)
    else:
        form = MeasurementForm()

    return render(request, 'measurement/measurement_form.html', {'form': form})


@login_required
def measurement_type_form(request):
    if request.method == 'POST':
        form = MeasurementTypeForm(request.POST)
        if form.is_valid():
            measurement_type = form.save(commit=False)
            measurement_type.user = request.user
            measurement_type.save()
            return home(request)
    else:
        form = MeasurementTypeForm()

    return render(request, 'measurement/measurement_type_form.html',
                  {'form': form})


def parse_csv(file):
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)
    date = 'date'
    units = 'units'
    obligatory_fields = [date, units]

    col_number = 3
    if len(reader.fieldnames) != col_number:
        raise ValueError("Wrong format. Csv file has to consist from 3 columns (order does't matter) "
                         "with names: date, units, measurement_type")

    measurements = []
    for row in reader:
        measurement = {}
        if '-' in row['date']:
            measurement[date] = datetime.strptime(row['date'], "%Y-%m-%d")
        elif '/' in row['date']:
            measurement[date] = datetime.strptime(row['date'], "%Y/%m/%d")
        for field in reader.fieldnames:
            if field not in obligatory_fields:
                measurement['measurement_type'] = field
                measurement['measurement'] = float(row[field].replace(',', '.'))
        measurement[units] = row[units]
        measurements.append(measurement)
    return measurements


def add_to_database(request, measurements):

    m_type = MeasurementType.objects.filter(name=measurements[0]['measurement_type'])
    if len(m_type) > 0:
        add_bulk_measurements(request, measurements, m_type[0])
    else:
        m_type = MeasurementType(
            name=measurements[0]['measurement_type'],
            user=request.user
        )
        m_type.save()
        # add_measurements(request, measurements, m_type)
        add_bulk_measurements(request, measurements, m_type)


def add_bulk_measurements(request, measurements, measurement_type):
    db_measurements = []
    for measurement in measurements:
        m = Measurement(
            user=request.user,
            units=measurement['units'],
            measurement_type=measurement_type,
            measurement=measurement['measurement']
        )
        db_measurements.append(m)
    Measurement.objects.bulk_create(db_measurements)


def add_measurements(request, measurements, measurement_type):
    for measurement in measurements:
        m = Measurement(
            user=request.user,
            units=measurement['units'],
            measurement_type=measurement_type,
            measurement=measurement['measurement']
        )
        m.save()


@login_required
def measurement_csv_form(request):
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            measurements = parse_csv(form.cleaned_data['file'])
            add_to_database(request, measurements)
            return render(request, 'measurement/measurement_csv_success.html', {
                'measurements': measurements,
            })
    else:
        form = CsvForm()

    return render(request, 'measurement/measurement_csv_form.html',
                  {'form': form})

