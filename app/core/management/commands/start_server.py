import os

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    # Django command to start the server from PyCharm
    def add_arguments(self, parser):
        parser.add_argument('host', nargs='+', type=str)

    def handle(self, *args, **options):
        # Run the pre-start commands only if the command is not
        # running in the process spawned by the auto-reloader.
        # This can be detected through an environment variable.
        if os.environ.get('RUN_MAIN') == 'true':
            call_command('wait_for_db')
            call_command('migrate')

        call_command('runserver', options.get('host')[0])
