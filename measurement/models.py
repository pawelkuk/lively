from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q


UNIT_CHOICES = (
    ('kg', 'kilograms'),
    ('lbs', 'pounds'),
    ('cm', 'centimeter'),
    ('m', 'meters'),
    ('in', 'inches'),
    ('ft', 'feet'),
)


class MeasurementType(models.Model):
    user = models.ForeignKey(
        User,
        related_name='measurement_type_user',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}".format(self.name)


class MeasurementQuerySet(models.QuerySet):
    def measurements_for_user(self, user):
        return self.filter(Q(user=user)).order_by('-creation_date')

    def measurements_for_user_with_type(self, user, measurement_type):
        return self.filter(user=user, measurement_type=measurement_type)


class Measurement(models.Model):
    user = models.ForeignKey(
        User,
        related_name='measurement_user',
        on_delete=models.CASCADE
    )
    measurement_type = models.ForeignKey(
        'MeasurementType',
        related_name='measurement_type',
        on_delete=models.CASCADE
    )
    note = models.CharField(max_length=300, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    measurement = models.IntegerField(
        validators=[MinValueValidator(0), ],
        blank=False, null=False
         )
    units = models.CharField(
        max_length=3,
        choices=UNIT_CHOICES)
    objects = MeasurementQuerySet.as_manager()

    def __str__(self):
        return "{0} {1} {2}".format(
            self.measurement_type,
            self.measurement,
            self.units
        )
