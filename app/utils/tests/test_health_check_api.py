from django.test import TestCase
from unittest.mock import patch

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse

import redis
from redis import ConnectionError

HEALTH_CHECK_URL = reverse('utils:health-check')
DATE_REGEX = '^(([0-9]{4})-([0-9]{2})-([0-9]{2}) (([0-9]{2}):([0-9]{2}):([0-9]{2})))?$'


class HealthCheckApiTest(TestCase):

    def setup(self):
        self.client = APIClient()

    def test_health_check_success(self):
        res = self.client.get(HEALTH_CHECK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'Ok')
        self.assertEqual(res.data['app_id'], '01-01-01')
        self.assertRegex(res.data['time'], DATE_REGEX)

    @patch('redis.StrictRedis.hget', side_effect=[ConnectionError])
    def test_health_check_component_failed(self, redis):

        res = self.client.get(HEALTH_CHECK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'Error')
        self.assertEqual(res.data['app_id'], '01-01-01')
        self.assertRegex(res.data['time'], DATE_REGEX)
