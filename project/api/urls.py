from django.urls import include
from django.urls import path
from django.urls import re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('products', views.ProductsViewSet)
router.register('lessons', views.LessonsViewSet)
router.register('lesson_views', views.LessonViewsViewSet)
router.register('stat', views.StatViewSet, basename='stat')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('stat/product/', views.ProductStatView.as_view()),
    path('stat/product/<int:pk>/', views.ProductStatView.as_view()),
    path('stat/lesson/', views.LessonStatView.as_view()),
    path('stat/lesson/<int:pk>/', views.LessonStatView.as_view()),
]

urlpatterns += router.urls
