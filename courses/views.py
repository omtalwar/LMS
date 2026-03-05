from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Enrollment, LessonCompletion, Category, Profile, Assignment, Submission, Attendance
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime



def signup_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    query = request.GET.get('q')
    category_name = request.GET.get('category')

    courses = Course.objects.all()
    categories = Category.objects.all()

    if query:
        courses = courses.filter(title__icontains=query)

    if category_name:
        courses = courses.filter(category__name=category_name)

    return render(request, 'home.html', {
        'courses': courses,
        'categories': categories
    })


def course_detail(request, id):

    course = get_object_or_404(Course, id=id)
    lessons = course.lesson_set.all()

    assignments = Assignment.objects.filter(course=course)

    is_enrolled = False
    completed_lessons = []

    if request.user.is_authenticated:

        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

        completed_lessons = list(
            LessonCompletion.objects.filter(
                user=request.user,
                lesson__course=course,
                completed=True
            ).values_list('lesson_id', flat=True)
        )

    total_lessons = lessons.count()
    completed_count = len(completed_lessons)

    progress = 0
    if total_lessons > 0:
        progress = int((completed_count / total_lessons) * 100)

    return render(request, 'course_detail.html', {
        'course': course,
        'lessons': lessons,
        'assignments': assignments,
        'is_enrolled': is_enrolled,
        'completed_lessons': completed_lessons,
        'progress': progress
    })


@login_required
def enroll_course(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return redirect('course_detail', id=course.id)


@login_required
def mark_complete(request, lesson_id):

    lesson = get_object_or_404(Lesson, id=lesson_id)

    LessonCompletion.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': True}
    )

    return redirect('course_detail', id=lesson.course.id)


@login_required
def dashboard(request):

    enrollments = Enrollment.objects.filter(user=request.user)

    data = []

    for enrollment in enrollments:

        course = enrollment.course
        lessons = Lesson.objects.filter(course=course)

        total = lessons.count()

        completed = LessonCompletion.objects.filter(
            user=request.user,
            lesson__course=course,
            completed=True
        ).count()

        progress = 0
        if total > 0:
            progress = int((completed / total) * 100)

        total_attendance = Attendance.objects.filter(
        student=request.user,
        lesson__course=course
        ).count()

        present_attendance = Attendance.objects.filter(
        student=request.user,
        lesson__course=course,
        status="present"
        ).count()

        attendance_percentage = 0
        if total_attendance > 0:
            attendance_percentage = int((present_attendance / total_attendance) * 100)

        data.append({
            'course': course,
            'progress': progress,
            'attendance': attendance_percentage
        })

    return render(request, 'dashboard.html', {
        'data': data
    })


# ADD COURSE
@login_required
def add_course(request):

    if request.user.profile.role != 'teacher':
        return redirect('home')

    categories = Category.objects.all()

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        thumbnail = request.POST.get('thumbnail')
        category_id = request.POST.get('category')

        category = Category.objects.get(id=category_id)

        Course.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            thumbnail=thumbnail,
            category=category
        )

        return redirect('dashboard')

    return render(request, 'add_course.html', {
        'categories': categories
    })


def lesson_detail(request, lesson_id):

    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course

    lessons = list(course.lesson_set.all())
    lesson_index = lessons.index(lesson) + 1

    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    is_completed = False

    if request.user.is_authenticated:
        is_completed = LessonCompletion.objects.filter(
            user=request.user,
            lesson=lesson,
            completed=True
        ).exists()

    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'course': course,
        'is_enrolled': is_enrolled,
        'lesson_index': lesson_index,
        'is_completed': is_completed
    })


@login_required
def add_lesson(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.user.profile.role != 'teacher':
        return redirect('home')

    if request.method == 'POST':

        title = request.POST.get('title')
        content = request.POST.get('content')
        video = request.FILES.get('video')

        Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            video=video
        )

        return redirect('course_detail', id=course.id)

    return render(request, 'add_lesson.html', {'course': course})


@login_required
def add_assignment(request, course_id):

    course = Course.objects.get(id=course_id)

    if request.user != course.teacher:
        return redirect('home')

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline_str = request.POST.get("deadline")
        file = request.FILES.get("file")

        deadline = datetime.fromisoformat(deadline_str)


        Assignment.objects.create(
            course=course,
            title=title,
            description=description,
            deadline=deadline,
            file=file
        )

        return redirect("course_detail", id=course.id)

    return render(request, "add_assignment.html", {"course": course})


@login_required
def assignment_detail(request, assignment_id):

    assignment = get_object_or_404(Assignment, id=assignment_id)

    submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    deadline_passed = timezone.now() > assignment.deadline

    return render(request, "assignment_detail.html", {
        "assignment": assignment,
        "submission": submission,
        "now": timezone.now()
    })

@login_required
def submit_assignment(request, assignment_id):

    assignment = get_object_or_404(Assignment, id=assignment_id)

    # 🔥 Block submissions after deadline
    if assignment.deadline <= timezone.now():
        return render(request, "submit_assignment.html", {
            "assignment": assignment,
            "error": "Deadline has passed. Submission closed."
    })

    # 🔥 If form submitted
    if request.method == "POST":

        file = request.FILES.get("file")

        if not file:
            return render(request, "submit_assignment.html", {
                "assignment": assignment,
                "error": "Please upload a file."
            })

        # prevent duplicate submission
        existing = Submission.objects.filter(
            assignment=assignment,
            student=request.user
        ).first()

        if existing:
            existing.file = file
            existing.save()
        else:
            Submission.objects.create(
                assignment=assignment,
                student=request.user,
                file=file
            )

        return redirect("assignment_detail", assignment_id=assignment.id)

    return render(request, "submit_assignment.html", {
        "assignment": assignment
    })

@login_required
def delete_assignment(request, assignment_id):

    assignment = get_object_or_404(Assignment, id=assignment_id)

    # only the teacher who created the course can delete
    if request.user != assignment.course.teacher:
        return redirect("home")

    course_id = assignment.course.id

    assignment.delete()

    return redirect("course_detail", id=course_id)

# TEACHER GRADING PANEL
@login_required
def assignment_submissions(request, assignment_id):

    assignment = Assignment.objects.get(id=assignment_id)

    submissions = Submission.objects.filter(
        assignment=assignment
    )

    if request.method == "POST":

        submission_id = request.POST.get("submission_id")
        marks = request.POST.get("marks")
        feedback = request.POST.get("feedback")

        submission = Submission.objects.get(id=submission_id)

        submission.marks = marks
        submission.feedback = feedback

        submission.save()

        return redirect("assignment_submissions", assignment_id=assignment.id)

    return render(request, "assignment_submissions.html", {
        "assignment": assignment,
        "submissions": submissions
    })


# ATTENDANCE SYSTEM
@login_required
def mark_attendance(request, lesson_id):

    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course

    if request.user != course.teacher:
        return redirect("home")

    students = Enrollment.objects.filter(course=course)

    if request.method == "POST":

        for student in students:

            status = request.POST.get(f"student_{student.user.id}")

            Attendance.objects.update_or_create(
                student=student.user,
                lesson=lesson,
                defaults={'status': status}
            )

        return redirect("lesson_detail", lesson_id=lesson.id)

    return render(request, "mark_attendance.html", {
        "lesson": lesson,
        "students": students
    })