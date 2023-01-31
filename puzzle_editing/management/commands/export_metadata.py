from django.core.management.base import BaseCommand

import puzzle_editing.utils as utils


class Command(BaseCommand):
    help = """Export metadata as JSON and push to Hunt repo."""

    def handle(self, *args, **options):
        utils.export_all()
