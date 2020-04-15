import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # Django commands to wait for database

    def handle(self, *args, **options):
        self.stdout.write('waiting for database...')
        db_cnx = None
        while not db_cnx:
            try:
                db_cnx = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting for 1 sec...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
