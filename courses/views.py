from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Enrollment, LessonCompletion, Category
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required



def signup_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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

    is_enrolled = False
    completed_lessons = []

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

        # 🔥 FIXED: convert queryset to list (important for production)
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
        'is_enrolled': is_enrolled,
        'completed_lessons': completed_lessons,
        'progress': progress
    })


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
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

        data.append({
            'course': course,
            'progress': progress,
            'completed': completed,
            'total': total
        })

    return render(request, 'dashboard.html', {
        'data': data
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