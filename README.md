# pythonHardQode

Учебный проект: REST API по работе с меню ресторана.\
Техническое задание: [spec.txt](./spec.txt).\
Схема данных: [schema.png](./schema.png).\
Технологии: Django, sqlite.


## Url для api по заданию
Общая статистика: 127.0.0.1:8000/stat/ \
Статистика по урокам: 127.0.0.1:8000/stat/lesson/{lesson_id}/ \
Статистика по продуктам: 127.0.0.1:8000/stat/product/{product_id}/

## Переменные среды
Для запуска и тестирования проекта, требуется создать файл `.env` с переменными окружения.\
Пример файла: `.env.example`

## База данные
Для запуска и тестирования проекта, требуется создать файл БД.\
Создание БД:
 - миграция;
 - переименуйте тестовую базу db.sqlite3.sample -> db.sqlite3

## Примечание
Для построения статистики использовались сырые запросы к БД.
Очевидно, что это не то, что хотели авторы задания, но построить такое через Django ORM
не получилось (на ORM sqlalchemy строится норм).

## Запуск через ком строку
```sh
./manage.py runserver
```
Перед запуском создайте файл переменных окружения (`.env`).\
Пример файла см. [Переменные среды](#пример-файла).
