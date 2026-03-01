from django.urls import path
from .views import home, course_detail,lesson_detail, login_view, logout_view, signup_view, enroll_course, mark_complete, dashboard

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
]