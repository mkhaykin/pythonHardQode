from django.contrib.auth.models import User
from django.db import models


class MixinTrack(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Products(MixinTrack):
    title = models.CharField(max_length=20, null=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fk_product_owner')
    students = models.ManyToManyField(User, related_name='fk_product_students', blank=True)
    lessons = models.ManyToManyField('Lessons', related_name='fk_product_lesson', blank=True)

    def get_students(self) -> str:
        return ', '.join([str(student) for student in self.students.all()])

    get_students.short_description = 'students'  # type: ignore

    def get_lessons(self) -> str:
        return ', '.join([str(lesson) for lesson in self.lessons.all()])

    get_lessons.short_description = 'lessons'    # type: ignore

    class Meta:
        app_label = 'api'
        verbose_name_plural = 'products'

    def __str__(self) -> str:
        return f'{self.title}'


class Lessons(MixinTrack):
    title = models.CharField(max_length=20, null=False, unique=True)
    video_url = models.TextField()
    video_duration = models.IntegerField(null=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        app_label = 'api'
        verbose_name_plural = 'lessons'

    def __str__(self) -> str:
        return f'{self.title}'


class LessonViews(MixinTrack):
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False)
    duration = models.IntegerField(null=False)
    is_finish = models.BooleanField(null=False, default=False)

    class Meta:
        app_label = 'api'
        verbose_name_plural = 'lessonview'

    def __str__(self) -> str:
        return f'{self.lesson}: {self.student}'
