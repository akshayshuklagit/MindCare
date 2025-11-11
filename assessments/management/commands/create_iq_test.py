from django.core.management.base import BaseCommand
from assessments.models import AssessmentType, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Create IQ Level Assessment'

    def handle(self, *args, **options):
        # Create IQ Assessment Type
        iq_assessment, created = AssessmentType.objects.get_or_create(
            short_name='IQ',
            defaults={
                'name': 'IQ Level Assessment',
                'description': 'A quick assessment to evaluate your cognitive abilities and problem-solving skills.',
                'instruction': 'Answer each question to the best of your ability. There is no time limit, but try to work efficiently.',
                'max_score': 150,
                'scoring_method': 'sum',
                'is_active': True,
                'requires_login': False,
                'estimated_time': 15,
            }
        )

        if created:
            self.stdout.write(f'Created IQ Assessment: {iq_assessment.name}')
        else:
            self.stdout.write(f'IQ Assessment already exists: {iq_assessment.name}')

        # IQ Test Questions
        questions_data = [
            {
                'text': 'What comes next in this sequence: 2, 4, 8, 16, ?',
                'choices': [
                    ('20', 5),
                    ('24', 8),
                    ('32', 15),
                    ('30', 10),
                ]
            },
            {
                'text': 'If all roses are flowers and some flowers fade quickly, which statement is definitely true?',
                'choices': [
                    ('All roses fade quickly', 5),
                    ('Some roses are flowers', 15),
                    ('No roses fade quickly', 8),
                    ('All flowers are roses', 3),
                ]
            },
            {
                'text': 'Which word does not belong: Apple, Orange, Banana, Carrot, Grape',
                'choices': [
                    ('Apple', 5),
                    ('Orange', 8),
                    ('Carrot', 15),
                    ('Grape', 10),
                ]
            },
            {
                'text': 'If you rearrange the letters "CIFAIPC", you would have the name of a:',
                'choices': [
                    ('Country', 8),
                    ('Ocean', 15),
                    ('City', 10),
                    ('Animal', 5),
                ]
            },
            {
                'text': 'What is 15% of 200?',
                'choices': [
                    ('25', 10),
                    ('30', 15),
                    ('35', 8),
                    ('20', 5),
                ]
            },
            {
                'text': 'Which number should come next: 1, 1, 2, 3, 5, 8, ?',
                'choices': [
                    ('11', 10),
                    ('13', 15),
                    ('12', 8),
                    ('10', 5),
                ]
            },
            {
                'text': 'Book is to Reading as Fork is to:',
                'choices': [
                    ('Drawing', 5),
                    ('Writing', 8),
                    ('Eating', 15),
                    ('Stirring', 10),
                ]
            },
            {
                'text': 'If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?',
                'choices': [
                    ('100 minutes', 5),
                    ('20 minutes', 8),
                    ('5 minutes', 15),
                    ('1 minute', 10),
                ]
            },
            {
                'text': 'Which shape completes the pattern: Circle, Square, Triangle, Circle, Square, ?',
                'choices': [
                    ('Circle', 8),
                    ('Triangle', 15),
                    ('Square', 10),
                    ('Rectangle', 5),
                ]
            },
            {
                'text': 'Mary is 16 years old. She is 4 times as old as her brother. How old will Mary be when she is twice as old as her brother?',
                'choices': [
                    ('20 years old', 10),
                    ('24 years old', 15),
                    ('18 years old', 8),
                    ('22 years old', 5),
                ]
            },
        ]

        # Create questions and choices
        for i, q_data in enumerate(questions_data, 1):
            question, created = Question.objects.get_or_create(
                assessment_type=iq_assessment,
                order=i,
                defaults={
                    'question_text': q_data['text'],
                    'is_required': True,
                    'is_active': True,
                }
            )

            if created:
                # Create answer choices
                for j, (choice_text, score) in enumerate(q_data['choices'], 1):
                    AnswerChoice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        score_value=score,
                        order=j
                    )
                self.stdout.write(f'Created question {i}: {q_data["text"][:50]}...')

        self.stdout.write(self.style.SUCCESS('IQ Assessment created successfully!'))