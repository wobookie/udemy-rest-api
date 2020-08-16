import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # Django commands to wait for database

    def handle(self, *args, **options):
        # Run the pre-start commands only if the command is not
        # running in the process spawned by the auto-reloader.
        # This can be detected through an environment variable.
        # if os.environ.get('RUN_MAIN') == 'true':

        logger.debug('waiting for database...')
        db_cnx = None
        while not db_cnx:
            try:
                db_cnx = connections['default']
            except OperationalError:
                logger.debug('Database unavailable, waiting for 1 sec...')
                time.sleep(1)

        logger.debug(self.style.SUCCESS('Database available'))
