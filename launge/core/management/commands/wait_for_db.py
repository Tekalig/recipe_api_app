"""
Django command to wait for the database to be available.
"""

import time
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError as DjangoError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to wait for the database to be available."""

    def handle(self, *args, **kwargs):
        """Handle the command."""
        self.stdout.write("Waiting for database...")

        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (DjangoError, Psycopg2Error):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
