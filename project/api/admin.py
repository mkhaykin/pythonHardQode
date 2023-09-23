from django.contrib import admin

from .models import Lessons
from .models import LessonViews
from .models import Products
# Register your models here.


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'get_students', 'get_lessons')


@admin.register(Lessons)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'video_url', 'video_duration', 'owner')


@admin.register(LessonViews)
class LessonViewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'student', 'start_time', 'duration', 'is_finish')
