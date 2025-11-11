from django.core.management.base import BaseCommand
from quotes.models import Quote

class Command(BaseCommand):
    help = 'Populate the database with Bhagavad Gita quotes'

    def handle(self, *args, **options):
        gita_quotes = [
            {
                'text': 'You have the right to perform your actions, but you are not entitled to the fruits of action.',
                'author': 'Bhagavad Gita 2.47',
                'category': 'mindfulness'
            },
            {
                'text': 'The mind is restless and difficult to restrain, but it is subdued by practice.',
                'author': 'Bhagavad Gita 6.35',
                'category': 'mindfulness'
            },
            {
                'text': 'When meditation is mastered, the mind is unwavering like the flame of a lamp in a windless place.',
                'author': 'Bhagavad Gita 6.19',
                'category': 'mindfulness'
            },
            {
                'text': 'A person can rise through the efforts of his own mind; or draw himself down, in the same manner.',
                'author': 'Bhagavad Gita 6.5',
                'category': 'self_care'
            },
            {
                'text': 'The soul is neither born, and nor does it die.',
                'author': 'Bhagavad Gita 2.20',
                'category': 'resilience'
            },
            {
                'text': 'Set thy heart upon thy work, but never on its reward.',
                'author': 'Bhagavad Gita 2.47',
                'category': 'motivation'
            },
            {
                'text': 'Man is made by his belief. As he believes, so he is.',
                'author': 'Bhagavad Gita 17.3',
                'category': 'positivity'
            },
            {
                'text': 'The happiness which comes from long practice, which leads to the end of suffering, is called supreme happiness.',
                'author': 'Bhagavad Gita 18.36',
                'category': 'positivity'
            }
        ]

        created_count = 0
        for quote_data in gita_quotes:
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
            self.style.SUCCESS(f'Successfully created {created_count} Gita quotes')
        )