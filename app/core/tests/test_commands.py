from unittest.mock import patch
from test.support import EnvironmentVarGuard
from io import StringIO

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set(envvar='RUN_MAIN', value='true')

    def test_wait_for_db_ready(self):
        # Test waiting for db when db is available
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            out = StringIO()
            call_command('wait_for_db', stdout=out)

            self.assertEquals(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        # Test waiting for db until ready
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            out = StringIO()
            call_command('wait_for_db', stdout=out)

            self.assertEquals(gi.call_count, 6)
