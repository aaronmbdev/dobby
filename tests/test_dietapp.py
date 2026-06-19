from unittest import TestCase

from src.integrations.diet.dietapp import DietAppClient


class TestDietAppClient(TestCase):
    def test_get_app_health(self):
        client = DietAppClient()
        health = client.get_app_health()
        assert health.get("status") == "ok"
