from django.urls import path
from .views import home, course_detail, lesson_detail, login_view, logout_view, signup_view, enroll_course, mark_complete, dashboard, add_course, add_lesson, add_assignment, assignment_detail, submit_assignment, assignment_submissions, delete_assignment, mark_attendance

urlpatterns = [
    path('', home, name='home'),
    path('course/<int:id>/', course_detail, name='course_detail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('complete/<int:lesson_id>/', mark_complete, name='mark_complete'),
    path('dashboard/', dashboard, name='dashboard'),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('add-course/', add_course, name='add_course'),
    path('add-lesson/<int:course_id>/', add_lesson, name='add_lesson'),
    path('add-assignment/<int:course_id>/', add_assignment, name='add_assignment'),
path('assignment/<int:assignment_id>/', assignment_detail, name='assignment_detail'),
path('submit-assignment/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
    path('assignment-submissions/<int:assignment_id>/', assignment_submissions, name='assignment_submissions'),
path('delete-assignment/<int:assignment_id>/', delete_assignment, name='delete_assignment'),
path('mark-attendance/<int:lesson_id>/', mark_attendance, name='mark_attendance'),
]