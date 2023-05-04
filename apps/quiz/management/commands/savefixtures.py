import os
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from quiz import auxiliary as auxi


class Command(BaseCommand):
    """
    Simimilar to dumpdata, but with tweeked usability:
        - use jsonlint, to generate readable json code,
        - ignore models on the hardcoded blacklist
        - use predefined path;

        - Note: there is also an option to download the backup-fixture (see quiz/urls.py)
    """
    help = 'Simimilar to dumpdata, but with tweeked usability.'

    def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('poll_ids', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--backup',
            action='store_true',
            help='save the result at settings.BACKUP_PATH and use datetime as filename.',
        )

    def handle(self, *args, **options):

        data_bytes = auxi.make_backup()

        if options.get('backup'):
            opfname = time.strftime("%Y-%m-%d__%H-%M-%S_backup_all.json")

            backup_path = settings.BACKUP_PATH
            os.makedirs(backup_path, exist_ok=True)

            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            outputpath = os.path.join(backup_path, opfname)
        else:
            outputpath = time.strftime("%Y-%m-%d__%H-%M-%S_all.json")


        # write bytes because we have specified utf8-encoding
        with open(outputpath, "wb") as jfile:
            jfile.write(data_bytes)

        self.stdout.write(f"file written: {outputpath}")
        self.stdout.write(self.style.SUCCESS('Done'))
