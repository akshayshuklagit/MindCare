from django.core.management.base import BaseCommand
from resources.models import ResourceCategory, Resource, CrisisResource
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate resources with sample data'

    def handle(self, *args, **options):
        self.create_categories()
        self.create_resources()
        self.create_crisis_resources()

        self.stdout.write(self.style.SUCCESS('Resources populated successfully!'))

    def create_categories(self):
        categories_data = [
            {
                'name': 'Anxiety Management',
                'description': 'Tools and information for depression',
                'icon': 'fas fa-brain',
                'color': 'blue',
                'order': 1
            },
            {
                'name': 'Depression Support',
                'description': 'Tools and information for depression',
                'icon': 'fas fa-heart',
                'color': 'purple',
                'order': 2
            },
            {
                'name': 'Stress Relief',
                'description': 'Techniques for managing stress',
                'icon': 'fas fa-leaf',
                'color': 'green',
                'order': 3
            },
            {
                'name': 'Sleep & Wellness',
                'description': 'Resources for better sleep and overall wellness',
                'icon': 'fas fa-moon',
                'color': 'indigo',
                'order': 4
            },
            {
                'name': 'Mindfulness',
                'description': 'Mindfulness and meditation resources',
                'icon': 'fas fa-om',
                'color': 'yellow',
                'order': 5
            }
        ]

        for cat_data in categories_data:
            category, created = ResourceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'order': cat_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

    def create_resources(self):
        anxiety_cat = ResourceCategory.objects.get(name='Anxiety Management')
        depression_cat = ResourceCategory.objects.get(name='Depression Support')
        stress_cat = ResourceCategory.objects.get(name='Stress Relief')

        resources_data = [
            {
                'title': 'Understanding Anxiety: A Complete Guide',
                'category': anxiety_cat,
                'resource_type': 'article',
                'summary': 'Learn about anxiety symptoms, causes, and effective management strategies.',
                'content' : 'Anxiety is a natural human response to uncertainty, yet when it begins to control our thoughts and emotions, it can cloud our peace of mind. This section is dedicated to helping you understand the nature of anxiety — not as an enemy, but as a messenger guiding you toward greater balance and self-awareness. Here, you’ll find insights into how anxious thoughts form, how they influence your body and emotions, and how to gently release their grip through awareness, compassion, and discipline. Drawing inspiration from both modern psychology and timeless wisdom like the Bhagavad Gita, we explore how inner calm can be cultivated even amidst life’s challenges. Through guided meditations, breathing exercises, reflective journaling prompts, and scientifically grounded strategies, you will learn to: Recognize early signs of anxiety and manage them before they escalate. Reframe negative thought patterns into constructive perspectives. Build resilience through mindfulness and emotional regulation techniques.Strengthen your connection to inner peace through self-acceptance and spiritual grounding. As Lord Krishna reminds us in the Gita, “Peace comes to those who are free from desire and anger, who have gained mastery over themselves.” This section invites you to walk that path — from restlessness to tranquility, from worry to wisdom, from reaction to reflection.',
                'difficulty_level': 'beginner',
                'estimated_read_time': 8,
                'tags': 'anxiety, mental health, coping strategies',
                'is_featured': True
            },
            {
                'title': 'Recognizing Depression Signs',
                'category': depression_cat,
                'resource_type': 'article',
                'summary': 'Learn to identify the signs of depression and understand when to seek help.',
                'content': 'Detailed information about depression symptoms and treatment options.',
                'difficulty_level': 'beginner',
                'estimated_read_time': 6,
                'tags': 'depression, symptoms, mental health',
                'is_featured': True
            },
            {
                'title': 'Daily Stress Management',
                'category': stress_cat,
                'resource_type': 'guide',
                'summary': 'Practical strategies to manage stress in your daily life.',
                'content': 'Evidence-based techniques for managing daily stress effectively.',
                'difficulty_level': 'intermediate',
                'estimated_read_time': 7,
                'tags': 'stress management, coping skills'
            }
        ]

        for resource_data in resources_data:
            resource, created = Resource.objects.get_or_create(
                title=resource_data['title'],
                defaults={
                    'slug': slugify(resource_data['title']),
                    'category': resource_data['category'],
                    'resource_type': resource_data['resource_type'],
                    'summary': resource_data['summary'],
                    'content': resource_data['content'],
                    'difficulty_level': resource_data['difficulty_level'],
                    'estimated_read_time': resource_data['estimated_read_time'],
                    'tags': resource_data['tags'],
                    'is_featured': resource_data.get('is_featured', False)
                }
            )
            if created:
                self.stdout.write(f'Created resource: {resource.title}')

    def create_crisis_resources(self):
        crisis_data = [
            {
                'name': 'Suicide & Crisis Lifeline',
                'phone_number': '988',
                'description': 'Free and confidential emotional support 24/7.',
                'availability': '24/7',
                'country': 'US',
                'is_crisis_line': True,
                'priority': 1
            },
            {
                'name': 'Crisis Text Line',
                'phone_number': '741741',
                'text_number': '741741',
                'description': 'Free, 24/7 support via text. Text HOME to 741741.',
                'availability': '24/7',
                'country': 'US',
                'is_crisis_line': True,
                'is_text_support': True,
                'priority': 2
            }
        ]

        for crisis in crisis_data:
            resource, created = CrisisResource.objects.get_or_create(
                name=crisis['name'],
                defaults=crisis
            )
            if created:
                self.stdout.write(f'Created crisis resource: {resource.name}')

