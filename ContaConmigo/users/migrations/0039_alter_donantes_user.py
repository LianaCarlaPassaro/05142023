# Generated by Django 4.2.3 on 2023-08-22 21:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0038_remove_donantes_user_donantes_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donantes',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
