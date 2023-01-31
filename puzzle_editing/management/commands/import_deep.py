import csv

from django.core.management.base import BaseCommand

from puzzle_editing.models import Puzzle


class Command(BaseCommand):
    help = """Import deep values from CSV."""

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        puzzle_mapping = {}
        with open(options["filename"]) as f:
            reader = csv.DictReader(f)
            for row in reader:
                puzzle_mapping[int(row["#"])] = {
                    "deep_key": row.get("Deep Key"),
                    "deep": int(row["Deep"]),
                }

        puzzles = Puzzle.objects.filter(id__in=puzzle_mapping.keys())
        for puzzle in puzzles:
            data = puzzle_mapping[puzzle.id]
            # Only override deep key if set
            # To unset, you have to do so manually in PuzzUp
            if data["deep_key"]:
                puzzle.deep_key = data["deep_key"]
            puzzle.deep = data["deep"]

        if puzzles:
            Puzzle.objects.bulk_update(puzzles, ["deep", "deep_key"])
            self.stdout.write(f"Successfully updated deep for {len(puzzles)} puzzles")

        unknown_keys = set(puzzle_mapping.keys()) - {puzzle.id for puzzle in puzzles}
        if unknown_keys:
            self.stdout.write(
                f"Warning: unable to find puzzles for ids: {unknown_keys}"
            )
