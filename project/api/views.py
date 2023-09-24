from typing import Any

from django.contrib.auth.models import User
from django.db import connection
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

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
    Конечная точка API, позволяющая просматривать или редактировать продукты.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class LessonsViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать или редактировать уроки.
    """
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer


class LessonViewsViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать или редактировать просмотр уроков.
    """
    queryset = LessonViews.objects.all()
    serializer_class = LessonViewsSerializer


def get_stat_user(product_id: int = 0, lesson_id: int = 0) -> list[dict[str, str | int]]:
    raw_sql = """
    SELECT
        api_products.id as product_id,
        api_products.title as product,
        api_lessons.id as lesson_id,
        api_lessons.title as lesson,
        auth_user.id as user_id,
        auth_user.username as username,
        lesson_stat.last_time as last_time,
        lesson_stat.max_duration as duration,
        lesson_stat.is_finish as is_finish
    FROM api_lessons
        INNER JOIN api_products_lessons	ON api_lessons.id = api_products_lessons.lessons_id
        INNER JOIN api_products ON api_products.id = api_products_lessons.products_id
        INNER JOIN api_products_students ON api_products.id = api_products_students.products_id
        INNER JOIN auth_user ON auth_user.id = api_products_students.user_id
        LEFT JOIN (
            SELECT
                student_id,
                lesson_id,
                MAX(is_finish) as is_finish,
                MAX(duration) as max_duration,
                MAX(start_time) as last_time
            FROM api_lessonviews
            GROUP BY student_id, lesson_id
        ) as lesson_stat ON api_lessons.id = lesson_stat.lesson_id AND auth_user.id = lesson_stat.student_id
    """
    params = []
    raw_where = 'WHERE True'
    if product_id:
        raw_where += ' AND api_products.id = %s '
        params.append(product_id)
    if lesson_id:
        raw_where += ' AND api_lessons.id = %s '
        params.append(lesson_id)

    with connection.cursor() as c:
        result = []
        keys = (
            'product_id', 'product',
            'lesson_id', 'lesson',
            'user_id', 'username',
            'last_time', 'duration', 'is_finish',
        )
        for row in c.execute(raw_sql + raw_where, params).fetchall():
            result.append(dict(zip(keys, row)))
    return result


def get_stat() -> list[dict[str, str | int]]:
    raw_sql = """
    SELECT
        api_products.title as product_id,
        api_products.title as product,
        COUNT(DISTINCT api_products_students.user_id) as students_count,
        ROUND(COUNT(DISTINCT api_products_students.user_id) * 1.0 /
            (SELECT COUNT(*) FROM auth_user), 2) as proc_buy,
        SUM(api_lessonviews.duration) as sum_time_view_sec
    FROM api_products
        LEFT JOIN api_products_students ON api_products_students.products_id = api_products.id
            OR api_products_students.products_id is NULL
        LEFT JOIN api_products_lessons ON api_products.id = api_products_lessons.products_id
        LEFT JOIN api_lessons ON api_lessons.id = api_products_lessons.lessons_id
        LEFT JOIN api_lessonviews ON api_lessonviews.lesson_id = api_lessons.id
    GROUP BY api_products.id, api_products.title;
    """
    with connection.cursor() as c:
        result = []
        keys = (
            'product_id', 'product',
            'students_count', 'proc_buy', 'sum_time_view_sec',
        )
        for row in c.execute(raw_sql).fetchall():
            result.append(dict(zip(keys, row)))
    return result


class LessonStatView(views.APIView):
    """
    Список всех уроков по всем продуктам к которым пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра.
    """
    def get(self, *args: Any, **kwargs: Any) -> Response:   # noqa: U100
        return Response(get_stat_user(lesson_id=kwargs.get('pk', 0)))


class ProductStatView(views.APIView):
    """
    Список уроков по конкретному продукту к которому пользователь имеет доступ,
    с выведением информации о статусе и времени просмотра, а также датой последнего просмотра ролика.
    """

    def get(self, *args: Any, **kwargs: Any) -> Response:   # noqa: U100
        return Response(get_stat_user(product_id=kwargs.get('pk', 0)))


class StatViewSet(viewsets.ViewSet):
    """
    Список всех продуктов на платформе, к каждому продукту приложить информацию:
     - количество просмотренных уроков от всех учеников.
     - сколько в сумме все ученики потратили времени на просмотр роликов.
     - количество учеников занимающихся на продукте.
    Процент приобретения продукта (рассчитывается исходя из количества полученных доступов к продукту деленное
    на общее количество пользователей на платформе).
    """
    def list(self, request: Any, format: Any | None = None) -> Response:    # noqa: A002, A003, U100
        return Response(get_stat())
