from django.core.management.base import BaseCommand
from courses.models import Course, Category, Lesson


class Command(BaseCommand):
    help = "Seed demo data"

    def handle(self, *args, **kwargs):

        # 📂 Categories
        web, _ = Category.objects.get_or_create(name="Web Development")
        design, _ = Category.objects.get_or_create(name="Design")

        # 📚 Courses with thumbnails
        course1, _ = Course.objects.get_or_create(
            title="Django Mastery",
            defaults={
                "description": "Learn Django from beginner to advanced",
                "category": web,
                "thumbnail": "https://images.unsplash.com/photo-1581276879432-15e50529f34b"
            }
        )

        course2, _ = Course.objects.get_or_create(
            title="UI/UX Design Basics",
            defaults={
                "description": "Learn modern UI design principles",
                "category": design,
                "thumbnail": "https://images.unsplash.com/photo-1559028012-481c04fa702d"
            }
        )

        # 🎥 Lessons for Course 1 (3 lessons)
        Lesson.objects.get_or_create(
            title="Intro to Django",
            course=course1,
            defaults={"content": "Getting started with Django"}
        )

        Lesson.objects.get_or_create(
            title="Models & ORM",
            course=course1,
            defaults={"content": "Understanding models and database"}
        )

        Lesson.objects.get_or_create(
            title="Views & Templates",
            course=course1,
            defaults={"content": "How Django renders pages"}
        )

        # 🎥 Lessons for Course 2 (3 lessons)
        Lesson.objects.get_or_create(
            title="Intro to UI/UX",
            course=course2,
            defaults={"content": "Basics of UI/UX design"}
        )

        Lesson.objects.get_or_create(
            title="Color & Typography",
            course=course2,
            defaults={"content": "Design fundamentals"}
        )

        Lesson.objects.get_or_create(
            title="Wireframing",
            course=course2,
            defaults={"content": "Creating layouts and flows"}
        )

        self.stdout.write(self.style.SUCCESS("✅ Demo data seeded successfully"))