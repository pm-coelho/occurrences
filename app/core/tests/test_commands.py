from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class MockGi():

    def ensure_connection(self):
        return True


class CommandTests(TestCase):

    def setUp(self):
        self.mock_gi = MockGi()
        pass

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = self.mock_gi
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # this patch decorator just speeds up the testing, moking the sleep time
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db to be ready before usage"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [self.mock_gi]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
