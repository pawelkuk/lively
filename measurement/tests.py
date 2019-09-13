from django.test import TransactionTestCase
from .models import Measurement
from unittest import TestCase


class MeasurementTransactionTest(TransactionTestCase):
    fixtures = ['measurement/fixtures/unit-test.json']

    def test_fixtures_load(self):
        self.assertTrue(Measurement.objects.count() > 0)
