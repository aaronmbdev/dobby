from unittest import TestCase

from src.integrations.diet.dietapp import DietAppClient


class TestDietAppClient(TestCase):

    def test_get_metrics(self):
        client = DietAppClient()
        metrics = client.get_body_metrics()
        assert isinstance(metrics, list)


    def test_get_daily_log(self):
        client = DietAppClient()
        test_date = "2026-06-18"
        daily_log = client.get_daily_log(test_date)
        assert isinstance(daily_log, dict)
