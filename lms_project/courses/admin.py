from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Course, Lesson, Enrollment, LessonCompletion, Category


# 🔥 Inline: Enrollments under User
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


# 🔥 Inline: Completed Lessons under User
class LessonCompletionInline(admin.TabularInline):
    model = LessonCompletion
    extra = 0


# 🔥 Custom User Admin
class CustomUserAdmin(UserAdmin):
    inlines = [EnrollmentInline, LessonCompletionInline]


# 🔥 Re-register User with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# 🔥 Inline Lessons inside Course
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    search_fields = ['title']
    list_filter = ['category']
    inlines = [LessonInline]


# 🔥 Register models
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment)
admin.site.register(LessonCompletion)
admin.site.register(Category)