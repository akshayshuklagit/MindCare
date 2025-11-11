from django.core.management.base import BaseCommand
from quotes.models import Quote

class Command(BaseCommand):
    help = 'Populate the database with sample inspirational quotes'

    def handle(self, *args, **options):
        quotes_data = [
            {
                'text': 'The only way to do great work is to love what you do.',
                'author': 'Steve Jobs',
                'category': 'motivation'
            },
            {
                'text': 'Mindfulness is a way of befriending ourselves and our experience.',
                'author': 'Jon Kabat-Zinn',
                'category': 'mindfulness'
            },
            {
                'text': 'You are braver than you believe, stronger than you seem, and smarter than you think.',
                'author': 'A.A. Milne',
                'category': 'self_care'
            },
            {
                'text': 'Anxiety is the dizziness of freedom.',
                'author': 'Søren Kierkegaard',
                'category': 'anxiety'
            },
            {
                'text': 'The present moment is the only time over which we have dominion.',
                'author': 'Thích Nhất Hạnh',
                'category': 'mindfulness'
            },
            {
                'text': 'Self-care is not selfish. You cannot serve from an empty vessel.',
                'author': 'Eleanor Brown',
                'category': 'self_care'
            },
            {
                'text': 'It is during our darkest moments that we must focus to see the light.',
                'author': 'Aristotle',
                'category': 'depression'
            },
            {
                'text': 'Positive anything is better than negative nothing.',
                'author': 'Elbert Hubbard',
                'category': 'positivity'
            },
            {
                'text': 'The strongest people are not those who show strength in front of us, but those who win battles we know nothing about.',
                'author': 'Unknown',
                'category': 'resilience'
            },
            {
                'text': 'Progress, not perfection.',
                'author': 'Unknown',
                'category': 'motivation'
            }
        ]

        created_count = 0
        for quote_data in quotes_data:
            quote, created = Quote.objects.get_or_create(
                text=quote_data['text'],
                defaults={
                    'author': quote_data['author'],
                    'category': quote_data['category']
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} quotes')
        )