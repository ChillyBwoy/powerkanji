import json
from pathlib import Path
from django.core.management.base import BaseCommand

from powerkanji.apps.kanji.models import Reading, Entity


class Command(BaseCommand):
    help = "Import data from json file"

    def add_arguments(self, parser):
        parser.add_argument("-f", dest="file_path")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        file_path = Path(file_path).resolve()

        with open(file_path, "r") as f:
            raw_entity_list = json.load(f)

            for raw_entity in raw_entity_list:
                entity = Entity.objects.create(
                    kanji=raw_entity["kanji"],
                    ext_id=raw_entity["ext_id"],
                    ext_key=raw_entity["key"],
                    strokes=raw_entity["strokes"],
                    jlpt=raw_entity["jlpt"],
                )

                for raw_onyomi in raw_entity["onyomi"]:
                    if len(raw_onyomi["reading"]) > 0:
                        Reading.objects.create(
                            reading=raw_onyomi["reading"],
                            meaning="\n".join(raw_onyomi["meanings"]),
                            kind=Reading.Kind.ONYOMI,
                            entity=entity,
                        )

                for raw_kunyomi in raw_entity["kunyomi"]:
                    if len(raw_kunyomi["reading"]) > 0:
                        Reading.objects.create(
                            reading=raw_kunyomi["reading"],
                            meaning="\n".join(raw_kunyomi["meanings"]),
                            kind=Reading.Kind.KUNYOMI,
                            entity=entity,
                        )
