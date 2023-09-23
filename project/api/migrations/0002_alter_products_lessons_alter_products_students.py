# Generated by Django 4.2.5 on 2023-09-23 05:17
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='lessons',
            field=models.ManyToManyField(
                blank=True, related_name='fk_product_lesson', to='api.lessons',
            ),
        ),
        migrations.AlterField(
            model_name='products',
            name='students',
            field=models.ManyToManyField(
                blank=True,
                related_name='fk_product_students',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]