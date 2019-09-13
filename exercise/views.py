from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from exercise.forms import BodyPartForm, ExerciseForm, LoadForm, SetForm
from exercise.models import BodyPart, Exercise, Load, Set
from user.views import home


@login_required
def body_part_form(request):
    if request.method == 'POST':
        form = BodyPartForm(request.POST)
        if form.is_valid():
            body_part = form.save(commit=False)
            body_part.user = request.user
            body_part.save()
            return home(request)
    else:
        form = BodyPartForm()

    return render(request, 'exercise/body_part_form.html', {'form': form})


@login_required
def set_form(request):
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            my_set = form.save(commit=False)
            my_set.user = request.user
            my_set.save()
            return home(request)
    else:
        form = SetForm()

    return render(request, 'exercise/set_form.html', {'form': form})


@login_required
def load_form(request):
    if request.method == 'POST':
        form = LoadForm(request.POST)
        if form.is_valid():
            load = form.save(commit=False)
            load.user = request.user
            load.save()
            return home(request)
    else:
        form = LoadForm()

    return render(request, 'exercise/load_form.html', {'form': form})


@login_required
def exercise_form(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return home(request)
    else:
        form = ExerciseForm()

    return render(request, 'exercise/exercise_form.html', {'form': form})

