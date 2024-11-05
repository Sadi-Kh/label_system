import csv
from django.core.management.base import BaseCommand
from api.models import Dataset, TextEntry, Tag


class Command(BaseCommand):
    help = 'Imports a dataset from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be imported.')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    # Get or create the dataset
                    dataset, _ = Dataset.objects.get_or_create(
                        name=row['name'],
                        defaults={'description': row['description']}
                    )

                    # Get or create the tag within this dataset
                    tag_name = row['tag']
                    tag, _ = Tag.objects.get_or_create(name=tag_name, dataset=dataset)

                    # Create a TextEntry and associate it with the tag and dataset
                    text_entry = TextEntry.objects.create(
                        dataset=dataset,
                        text=row['description']
                    )
                    text_entry.tags.add(tag)  # Link the tag to the entry

                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully added entry: {row["name"]} with tag: {tag_name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file_path}"))
