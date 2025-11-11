from django.core.management.base import BaseCommand
from assessments.models import AssessmentType, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Create Personality Type Assessment'

    def handle(self, *args, **options):
        # Create Personality Assessment Type
        personality_assessment, created = AssessmentType.objects.get_or_create(
            short_name='PERS',
            defaults={
                'name': 'Personality Type Assessment',
                'description': 'Discover your personality type and understand your behavioral patterns, preferences, and strengths.',
                'instruction': 'Choose the answer that best describes you or how you typically behave in most situations.',
                'max_score': 80,
                'scoring_method': 'sum',
                'is_active': True,
                'requires_login': False,
                'estimated_time': 10,
            }
        )

        if created:
            self.stdout.write(f'Created Personality Assessment: {personality_assessment.name}')
        else:
            self.stdout.write(f'Personality Assessment already exists: {personality_assessment.name}')

        # Personality Test Questions
        questions_data = [
            {
                'text': 'In social situations, you tend to:',
                'choices': [
                    ('Seek out new people to meet', 8),
                    ('Stay with people you know well', 6),
                    ('Find a quiet corner to observe', 4),
                    ('Leave early when possible', 2),
                ]
            },
            {
                'text': 'When making decisions, you usually:',
                'choices': [
                    ('Go with your gut feeling', 6),
                    ('Analyze all available data', 8),
                    ('Ask others for their opinions', 4),
                    ('Avoid making the decision', 2),
                ]
            },
            {
                'text': 'Your ideal weekend would involve:',
                'choices': [
                    ('An adventure or new experience', 8),
                    ('Relaxing at home with a book', 6),
                    ('Spending time with close friends', 4),
                    ('Catching up on work or chores', 2),
                ]
            },
            {
                'text': 'When working on a project, you prefer to:',
                'choices': [
                    ('Work independently', 6),
                    ('Collaborate with a team', 8),
                    ('Have clear instructions to follow', 4),
                    ('Wing it and see what happens', 2),
                ]
            },
            {
                'text': 'Your approach to planning is:',
                'choices': [
                    ('Plan everything in detail', 8),
                    ('Have a general outline', 6),
                    ('Keep things flexible', 4),
                    ('Prefer spontaneity', 2),
                ]
            },
            {
                'text': 'When facing a challenge, you:',
                'choices': [
                    ('Tackle it head-on immediately', 8),
                    ('Think it through carefully first', 6),
                    ('Seek advice from others', 4),
                    ('Hope it resolves itself', 2),
                ]
            },
            {
                'text': 'In conversations, you tend to:',
                'choices': [
                    ('Do most of the talking', 8),
                    ('Listen more than you speak', 6),
                    ('Ask lots of questions', 4),
                    ('Stay quiet unless asked', 2),
                ]
            },
            {
                'text': 'Your learning style is:',
                'choices': [
                    ('Hands-on experience', 8),
                    ('Reading and research', 6),
                    ('Discussion and debate', 4),
                    ('Visual aids and examples', 2),
                ]
            },
            {
                'text': 'When stressed, you typically:',
                'choices': [
                    ('Take action to solve the problem', 8),
                    ('Take time to think and reflect', 6),
                    ('Talk to someone about it', 4),
                    ('Try to distract yourself', 2),
                ]
            },
            {
                'text': 'Your ideal work environment is:',
                'choices': [
                    ('Fast-paced and dynamic', 8),
                    ('Quiet and organized', 6),
                    ('Collaborative and social', 4),
                    ('Flexible and autonomous', 2),
                ]
            },
        ]

        # Create questions and choices
        for i, q_data in enumerate(questions_data, 1):
            question, created = Question.objects.get_or_create(
                assessment_type=personality_assessment,
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

        self.stdout.write(self.style.SUCCESS('Personality Assessment created successfully!'))