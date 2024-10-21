from django.core.management.base import BaseCommand
from django.db import connections, OperationalError
import time


class Command(BaseCommand):
    help = "Waits for database to be ready for connection"

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for DB connection...")

        db_conn = connections["default"]

        while True:
            try:
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS("DB connection established."))
                break
            except OperationalError:
                self.stdout.write("Database unavailable, waiting...")
                time.sleep(0.1)
