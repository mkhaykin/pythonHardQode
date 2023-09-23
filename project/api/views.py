# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Lessons
from .models import LessonViews
from .models import Products
from .serializers import LessonSerializer
from .serializers import LessonViewsSerializer
from .serializers import ProductSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать или редактировать пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать или редактировать пользователей.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class LessonsViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать или редактировать пользователей.
    """
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer


class LessonViewsViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать или редактировать пользователей.
    """
    queryset = LessonViews.objects.all()
    serializer_class = LessonViewsSerializer
