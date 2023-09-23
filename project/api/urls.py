from django.urls import include
from django.urls import re_path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('products', views.ProductsViewSet)
router.register('lessons', views.LessonsViewSet)
router.register('lesson_views', views.LessonViewsViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
