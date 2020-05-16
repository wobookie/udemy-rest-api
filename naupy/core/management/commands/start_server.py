import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management import call_command

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # Django command to start the server from PyCharm
    def add_arguments(self, parser):
        parser.add_argument('host', type=str)
        parser.add_argument('--create-admin-account', action='store_true', help='Create an admin account')

    def handle(self, *args, **options):
        # Run the pre-start commands only if the command is not
        # running in the process spawned by the auto-reloader.
        # This can be detected through an environment variable.
        if os.environ.get('RUN_MAIN') == 'true':
            call_command('wait_for_db')
            call_command('migrate')

            # Django uses argpass
            # Argpass converts '-' into '_'
            if options['create_admin_account']:
                admin_user = os.environ.get('DJANGO_SUPERUSER_NAME')

                # create an admin user
                try:
                    call_command('createsuperuser', interactive=False, username=admin_user)
                    logger.debug('Admin account created...')
                except CommandError as error:
                    logger.debug('Could not create admin account, account might exists already. check logs for mor information...')
                    logger.debug('Error: ' + str(error))
                    pass

            # collect static files
            try:
                call_command('collectstatic', interactive=False, clear=True, link=True)
                logger.debug('Statics collected...')
            except CommandError as error:
                logger.debug('Could not collect static files...')
                logger.debug('Error: ' + str(error))
                pass

        if 'APP_ADRPORT' in os.environ:
            call_command('runserver', addrport=os.environ.get('APP_ADRPORT'))
        else:
            call_command('runserver')
