from unittest import TestCase

from src.integrations.diet.dietapp import DietAppClient


class TestDietAppClient(TestCase):
    def test_get_app_health(self):
        client = DietAppClient()
        health = client.get_app_health()
        assert health.get("status") == "ok"


    def test_get_metrics(self):
        client = DietAppClient()
        metrics = client.get_body_metrics()
        assert isinstance(metrics, dict)


    def test_get_daily_log(self):
        client = DietAppClient()
        test_date = "2026-06-18"
        daily_log = client.get_daily_log(test_date, test_date)
        assert isinstance(daily_log, dict)
