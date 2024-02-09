"""Django command to wait for the database to be available"""

from psycopg2 import OperationalError as psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entry point for command"""
        self.stdout.write("Waititng for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (psycopg2OpError, OperationalError):
                self.stdout.write("Database is unavailable")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database is available"))
