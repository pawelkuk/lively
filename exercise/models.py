from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q


UNIT_CHOICES = (
    ('kg', 'kilograms'),
    ('lbs', 'pounds'),
    ('bdw', 'bodyweight'),
)


class BodyPart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='body_part_user',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}".format(self.name)


class Exercise(models.Model):
    user = models.ForeignKey(
        User,
        related_name='exercise_user',
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(max_length=30, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    body_part = models.ForeignKey('BodyPart',
                                  related_name='exercise_body_part',
                                  on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_bodyweight = models.BooleanField(editable=True)

    def __str__(self):
        return "{0}".format(self.name)


class SetQuerySet(models.QuerySet):
    def sets_for_user(self, user):
        return self.filter(Q(user=user)).order_by('-date')

    def sets_for_user_with_type(self, user, exercise):
        return self.filter(user=user, exercise=exercise)


class Set(models.Model):
    user = models.ForeignKey(
        User,
        related_name='set_user',
        on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(
        'Exercise',
        related_name='set_exercise',
        on_delete=models.CASCADE
    )
    load = models.ForeignKey(
        'Load',
        related_name='set_load',
        on_delete=models.CASCADE
    )
    number_of_reps = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)])
    date = models.DateTimeField(auto_now_add=True)
    objects = SetQuerySet.as_manager()

    def __str__(self):
        return "{0} {1}".format(
            self.number_of_reps, self.exercise)


class Load(models.Model):
    user = models.ForeignKey(
        User,
        related_name='load_user',
        on_delete=models.CASCADE
    )
    load = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        blank=True, null=True
         )
    units = models.CharField(
        max_length=3,
        default='kg',
        choices=UNIT_CHOICES)

    def __str__(self):
        return "{0} {1}".format(
            self.load, self.units)
