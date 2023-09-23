from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Lessons
from .models import LessonViews
from .models import Products


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'groups')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'url', 'title', 'owner', 'students', 'lessons')


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lessons
        fields = ('id', 'url', 'title', 'owner', 'video_url', 'video_duration')


class LessonViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LessonViews
        fields = ('id', 'url', 'lesson', 'student', 'start_time', 'duration')
