from exercise.models import Load, Set, BodyPart, Exercise
from django.forms import ModelForm


class LoadForm(ModelForm):
    class Meta:
        model = Load
        fields = ['load', 'units']


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['exercise', 'load', 'number_of_reps']


class BodyPartForm(ModelForm):
    class Meta:
        model = BodyPart
        fields = ['name', 'description']


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'body_part', 'description', 'is_bodyweight']


class ExerciseProgressForm(ModelForm):
    class Meta:
        model = Set
        fields = ['exercise']
