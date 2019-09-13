from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

from datetime import date
import operator

from exercise.models import Set, Exercise, BodyPart, Load
from measurement.models import Measurement, MeasurementType
from measurement.forms import MeasurementProgressForm
from exercise.forms import ExerciseProgressForm


@login_required
def home(request):
    if len(MeasurementType.objects.all()) == 0 or \
            len(Exercise.objects.all()) == 0 or \
            len(BodyPart.objects.all()) == 0:
        pre_populate_measurements(request)
        pre_populate_exercise(request)
    my_sets = Set.objects.sets_for_user(request.user)
    if len(my_sets) > 10:
        my_sets = my_sets[:10]
    my_measurements = Measurement.objects.measurements_for_user(request.user)
    if len(my_measurements) > 10:
        my_measurements = my_measurements[:10]
    return render(request, 'user/home.html',
                  {'my_sets': my_sets,
                   'my_measurements': my_measurements})


@login_required
def measurement_progress(request):
    if request.method == 'POST':
        form = MeasurementProgressForm(request.POST)
        if form.is_valid():
            measurement_id = form.cleaned_data['measurement_type'].id
            return HttpResponseRedirect(''.join(('measurement/', str(measurement_id), '/')))
    else:
        form = MeasurementProgressForm()

    return render(request, 'measurement/measurement_progress_form.html', {'form': form})


@login_required
def exercise_progress(request):
    if request.method == 'POST':
        form = ExerciseProgressForm(request.POST)
        if form.is_valid():
            exercise_id = form.cleaned_data['exercise'].id
            return HttpResponseRedirect(''.join(('exercise/', str(exercise_id), '/')), {type: id})
    else:
        form = ExerciseProgressForm()

    return render(request, 'exercise/exercise_progress_form.html', {'form': form})


def _check_if_has_permission(request, progress_type):
    # TODO
    pass


class DataPoint:
    def __init__(self, label, data, enum):
        self.data = data
        self.label = label
        self.enum = enum


@login_required
def progress_measurement_chart(request, progress_type):
    _check_if_has_permission(request, progress_type)
    my_measurements = Measurement.objects.measurements_for_user_with_type(request.user, progress_type)
    if len(my_measurements) == 0:
        return HttpResponse(str(progress_type))
    ordered_measurements = sorted(my_measurements, key=operator.attrgetter('creation_date'))
    label = str(ordered_measurements[0].measurement_type)
    data_points = []
    i = 0
    for measurement in ordered_measurements:
        tmp_data = measurement.measurement
        tmp_label = str(date(
            year=measurement.creation_date.year,
            month=measurement.creation_date.month,
            day=measurement.creation_date.day
        ))
        data_points.append(DataPoint(
            label=tmp_label,
            data=tmp_data,
            enum=i
        ))
        i += 1
    return render(request, 'user/progress.html', {'label': label,
                                                  'data_points': data_points})


@login_required
def progress_exercise_chart(request, progress_type):
    _check_if_has_permission(request, progress_type)
    my_sets = Set.objects.sets_for_user_with_type(request.user, progress_type)
    if len(my_sets) == 0:
        return HttpResponse(str(progress_type))
    ordered_sets = sorted(my_sets, key=operator.attrgetter('date'))
    label = str(ordered_sets[0].exercise.name)
    data_points = []
    i = 0
    for my_set in ordered_sets:
        tmp_data = my_set.load.load
        tmp_label = str(date(
            year=my_set.date.year,
            month=my_set.date.month,
            day=my_set.date.day
        ))
        data_points.append(DataPoint(
            label=tmp_label,
            data=tmp_data,
            enum=i
        ))
        i += 1
    return render(request, 'user/progress.html', {'label': label,
                                                  'data_points': data_points})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/signup_form.html'
    success_url = reverse_lazy('user_home')


def pre_populate_measurements(request):
    default_types = [
        'chest',
        'weight',
        'hips',
        'calves',
        'forearm',
        'stomach',
        'thigh',
        'height',
        'kcal intake',
        'wrist',
    ]
    types_list = []
    for default_type in default_types:
        m = MeasurementType(user=request.user,
                            name=default_type)
        types_list.append(m)
    MeasurementType.objects.bulk_create(types_list)


def pre_populate_exercise(request):
    pre_populate_bodyparts(request)
    pre_populate_exercises(request)
    pre_populate_loads(request)


def pre_populate_bodyparts(request):
    default_types = [
        'arms',
        'forearms',
        'shoulders',
        'neck',
        'traps',
        'back',
        'delts',
        'lower back',
        'biceps',
        'triceps',
        'rotator cuff',
        'abs',
        'obliques',
        'legs',
        'calves',
        'chest',
        'hamstrings',
        'butt',
        'full body',
    ]
    types_list = []
    for default_type in default_types:
        m = BodyPart(user=request.user,
                     name=default_type)
        types_list.append(m)
    BodyPart.objects.bulk_create(types_list)


def pre_populate_exercises(request):
    default_types = [
        'squads',
        'deadlift',
        'biceps curl',
        'crunches',
        'calf raises',
        'adduction',
        'abduction',
        'overhead press',
    ]
    types_list = []
    for default_type in default_types:
        m = Exercise(user=request.user,
                     name=default_type,
                     body_part=BodyPart.objects.filter(name='full body')[0],
                     is_bodyweight=False)
        types_list.append(m)
    Exercise.objects.bulk_create(types_list)


def pre_populate_loads(request):
    default_types = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
    ]
    types_list = []
    for default_type in default_types:
        m = Load(user=request.user,
                 load=default_type)
        types_list.append(m)
    Load.objects.bulk_create(types_list)
