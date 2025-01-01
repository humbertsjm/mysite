# pylint: skip-file
import json
from typing import Any

from django.core.management.base import BaseCommand

from apps.coreapp.models.json_models import SeedJSON


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        JSON_PATH = 'seed.json'
        json_data: SeedJSON = None

        # from ._private import create_seed_object
        # json_data = create_seed_object()

        with open(JSON_PATH, 'w') as json_file:
            obj: dict[str, Any] = json_data.to_dict()
            json.dump(json_data.to_dict(), json_file)
