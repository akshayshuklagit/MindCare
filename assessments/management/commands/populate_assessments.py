from django.core.management.base import BaseCommand
from assessments.models import AssessmentType, Question, AnswerChoice, EmergencyResource


class Command(BaseCommand):
    help = 'Populate database with PHQ-9 and GAD-7 assessment questions'

    def handle(self, *args, **options):
        self.stdout.write('Starting assessment population...')
        
        # Create PHQ-9 Assessment
        self.create_phq9()
        
        # Create GAD-7 Assessment
        self.create_gad7()
        
        # Create Emergency Resources
        self.create_emergency_resources()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated assessment data!')
        )

    def create_phq9(self):
        """Create PHQ-9 (Patient Health Questionnaire-9) assessment."""
        self.stdout.write('Creating PHQ-9 assessment...')
        
        # Create or get PHQ-9 assessment type
        phq9, created = AssessmentType.objects.get_or_create(
            short_name='PHQ9',
            defaults={
                'name': 'Patient Health Questionnaire-9',
                'description': 'The PHQ-9 is a widely used instrument for screening, diagnosing, monitoring and measuring the severity of depression.',
                'instruction': 'Over the last 2 weeks, how often have you been bothered by any of the following problems?',
                'max_score': 27,
                'scoring_method': 'sum',
                'estimated_time': 5,
                'requires_login': False,
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(f'Created PHQ-9 assessment type')

        # PHQ-9 Questions
        phq9_questions = [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep, or sleeping too much",
            "Feeling tired or having little energy",
            "Poor appetite or overeating",
            "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
            "Trouble concentrating on things, such as reading the newspaper or watching television",
            "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
            "Thoughts that you would be better off dead or of hurting yourself in some way"
        ]

        # Answer choices for PHQ-9 (same for all questions)
        phq9_choices = [
            ("Not at all", 0),
            ("Several days", 1),
            ("More than half the days", 2),
            ("Nearly every day", 3)
        ]

        # Create questions and answer choices
        for i, question_text in enumerate(phq9_questions, 1):
            question, created = Question.objects.get_or_create(
                assessment_type=phq9,
                order=i,
                defaults={
                    'question_text': question_text,
                    'is_required': True,
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(f'Created PHQ-9 question {i}')
                
                # Create answer choices for this question
                for j, (choice_text, score) in enumerate(phq9_choices, 1):
                    AnswerChoice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        score_value=score,
                        order=j
                    )

    def create_gad7(self):
        """Create GAD-7 (Generalized Anxiety Disorder 7-item) assessment."""
        self.stdout.write('Creating GAD-7 assessment...')
        
        # Create or get GAD-7 assessment type
        gad7, created = AssessmentType.objects.get_or_create(
            short_name='GAD7',
            defaults={
                'name': 'Generalized Anxiety Disorder 7-item',
                'description': 'The GAD-7 is a screening tool for generalized anxiety disorder and a severity measure for anxiety symptoms.',
                'instruction': 'Over the last 2 weeks, how often have you been bothered by the following problems?',
                'max_score': 21,
                'scoring_method': 'sum',
                'estimated_time': 3,
                'requires_login': False,
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(f'Created GAD-7 assessment type')

        # GAD-7 Questions
        gad7_questions = [
            "Feeling nervous, anxious or on edge",
            "Not being able to stop or control worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Being so restless that it is hard to sit still",
            "Becoming easily annoyed or irritable",
            "Feeling afraid as if something awful might happen"
        ]

        # Answer choices for GAD-7 (same as PHQ-9)
        gad7_choices = [
            ("Not at all", 0),
            ("Several days", 1),
            ("More than half the days", 2),
            ("Nearly every day", 3)
        ]

        # Create questions and answer choices
        for i, question_text in enumerate(gad7_questions, 1):
            question, created = Question.objects.get_or_create(
                assessment_type=gad7,
                order=i,
                defaults={
                    'question_text': question_text,
                    'is_required': True,
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(f'Created GAD-7 question {i}')
                
                # Create answer choices for this question
                for j, (choice_text, score) in enumerate(gad7_choices, 1):
                    AnswerChoice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        score_value=score,
                        order=j
                    )

    def create_emergency_resources(self):
        """Create emergency mental health resources."""
        self.stdout.write('Creating emergency resources...')
        
        emergency_resources = [
            {
                'name': 'National Suicide Prevention Lifeline',
                'phone_number': '988',
                'description': 'Free and confidential emotional support for people in suicidal crisis or emotional distress 24 hours a day, 7 days a week.',
                'availability': '24/7',
                'country': 'US',
                'is_crisis_line': True,
                'priority': 1,
            },
            {
                'name': 'Crisis Text Line',
                'phone_number': 'Text HOME to 741741',
                'description': 'Free, 24/7 crisis support via text message. Trained crisis counselors provide support for mental health crises.',
                'availability': '24/7',
                'country': 'US',
                'is_crisis_line': True,
                'priority': 2,
            },
            {
                'name': 'SAMHSA National Helpline',
                'phone_number': '1-800-662-4357',
                'description': 'Free, confidential, 24/7 treatment referral and information service for individuals and families facing mental health and/or substance use disorders.',
                'availability': '24/7',
                'country': 'US',
                'is_crisis_line': False,
                'priority': 3,
            },
            {
                'name': 'National Alliance on Mental Illness (NAMI) Helpline',
                'phone_number': '1-800-950-6264',
                'description': 'Information, resource referrals and support for individuals and families affected by mental illness.',
                'availability': 'Monday-Friday 10am-10pm ET',
                'country': 'US',
                'is_crisis_line': False,
                'priority': 4,
            },
            {
                'name': 'Veterans Crisis Line',
                'phone_number': '1-800-273-8255 (Press 1)',
                'description': 'Free, confidential support for veterans in crisis, their families and friends 24/7.',
                'availability': '24/7',
                'country': 'US',
                'is_crisis_line': True,
                'priority': 5,
            }
        ]
        
        for resource_data in emergency_resources:
            resource, created = EmergencyResource.objects.get_or_create(
                name=resource_data['name'],
                defaults=resource_data
            )
            if created:
                self.stdout.write(f'Created emergency resource: {resource.name}')
