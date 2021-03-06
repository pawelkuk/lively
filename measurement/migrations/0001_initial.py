# Generated by Django 2.2.4 on 2019-08-22 11:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurement_type_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, max_length=300, null=True)),
                ('measurement', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('units', models.CharField(choices=[('kg', 'kilograms'), ('lbs', 'pounds'), ('cm', 'centimeter'), ('m', 'meters'), ('in', 'inches'), ('ft', 'feet')], max_length=3)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('measurement_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurement_type', to='measurement.MeasurementType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurement_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
