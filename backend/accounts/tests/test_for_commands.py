from django.test import SimpleTestCase
from psycopg2 import OperationalError as psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from unittest.mock import patch
import time

# Create your tests here.


class CommandTest(SimpleTestCase):
    @patch("account.management.commands.wait_for_db.Command.check")
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if the database is ready"""
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    @patch.object(time, "sleep")
    @patch("account.management.commands.wait_for_db.Command.check")
    def test_wait_for_db_delay(self, patched_check, patched_sleep):
        """Test waiting for the database when getting operational Error"""
        patched_check.side_effect = (
            [psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
