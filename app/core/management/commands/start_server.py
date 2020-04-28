import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management import call_command

import logging
logger = logging.getLogger('app_logger')

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

                try:
                    call_command('createsuperuser', interactive=False, username=admin_user)
                    logger.debug('Admin account created...')
                except CommandError as error:
                    logger.debug('Could not create admin account, account might exists already. check logs for mor information...')
                    logger.debug('Error: ' + str(error))
                    pass

        call_command('runserver', options.get('host'))
