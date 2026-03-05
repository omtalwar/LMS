from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from pathlib import Path
from django.core.files import File

from courses.models import (
    Course,
    Category,
    Lesson,
    Enrollment,
    Assignment,
    Profile,
    Attendance
)


class Command(BaseCommand):
    help = "Seed LMS demo data"


    def handle(self, *args, **kwargs):

        # -------------------------------
        # USERS
        # -------------------------------

        teacher, created = User.objects.get_or_create(username="teacher")
        if created:
            teacher.set_password("password123")
            teacher.save()

        Profile.objects.update_or_create(
            user=teacher,
            defaults={"role": "teacher"}
        )


        student, created = User.objects.get_or_create(username="student")
        if created:
            student.set_password("password123")
            student.save()

        Profile.objects.update_or_create(
            user=student,
            defaults={"role": "student"}
        )


        # -------------------------------
        # CATEGORY
        # -------------------------------

        web, _ = Category.objects.get_or_create(
            name="Web Development"
        )


        # -------------------------------
        # COURSE
        # -------------------------------

        course, _ = Course.objects.get_or_create(
            title="Django Full Course",
            defaults={
                "description": "Complete Django course covering backend development",
                "teacher": teacher,
                "category": web,
                "thumbnail": "https://images.unsplash.com/photo-1581276879432-15e50529f34b"
            }
        )


        # -------------------------------
        # VIDEO FILE
        # -------------------------------

        video_path = Path("media/videos/demo.mp4")


        # -------------------------------
        # LESSONS
        # -------------------------------

        if video_path.exists():

            with open(video_path, "rb") as video:

                lesson1, _ = Lesson.objects.get_or_create(
                    title="Introduction to Django",
                    course=course,
                    defaults={
                        "content": "Overview of Django framework",
                        "video": File(video, name="demo.mp4")
                    }
                )

            with open(video_path, "rb") as video:

                lesson2, _ = Lesson.objects.get_or_create(
                    title="Models and Database",
                    course=course,
                    defaults={
                        "content": "Working with Django ORM",
                        "video": File(video, name="demo.mp4")
                    }
                )

            with open(video_path, "rb") as video:

                lesson3, _ = Lesson.objects.get_or_create(
                    title="Views and Templates",
                    course=course,
                    defaults={
                        "content": "Rendering HTML with Django"
                    }
                )

        else:

            lesson1, _ = Lesson.objects.get_or_create(
                title="Introduction to Django",
                course=course,
                defaults={"content": "Overview of Django framework"}
            )

            lesson2, _ = Lesson.objects.get_or_create(
                title="Models and Database",
                course=course,
                defaults={"content": "Working with Django ORM"}
            )

            lesson3, _ = Lesson.objects.get_or_create(
                title="Views and Templates",
                course=course,
                defaults={"content": "Rendering HTML with Django"}
            )


        # -------------------------------
        # ENROLL STUDENT
        # -------------------------------

        Enrollment.objects.get_or_create(
            user=student,
            course=course
        )


        # -------------------------------
        # ASSIGNMENTS
        # -------------------------------

        expired_deadline = timezone.now() - timedelta(days=1)
        future_deadline = timezone.now() + timedelta(days=5)


        Assignment.objects.get_or_create(
            title="Django Basics Assignment",
            course=course,
            defaults={
                "description": "Build a simple Django application",
                "deadline": expired_deadline
            }
        )


        Assignment.objects.get_or_create(
            title="Django Blog Project",
            course=course,
            defaults={
                "description": "Create a blog system using Django",
                "deadline": future_deadline
            }
        )


        # -------------------------------
        # ATTENDANCE
        # -------------------------------

        Attendance.objects.get_or_create(
            student=student,
            lesson=lesson1,
            defaults={"status": "present"}
        )

        Attendance.objects.get_or_create(
            student=student,
            lesson=lesson2,
            defaults={"status": "present"}
        )

        Attendance.objects.get_or_create(
            student=student,
            lesson=lesson3,
            defaults={"status": "absent"}
        )


        self.stdout.write(
            self.style.SUCCESS("✅ Demo LMS data created successfully")
        )