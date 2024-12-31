# pylint: skip-file
import subprocess

from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:

        subprocess.run([
            "isort",
            "apps",
        ])

        subprocess.run([
            "pylint",
            "apps",
            "--rcfile=.pylintrc"
        ])
