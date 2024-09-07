# Generated by Django 5.1 on 2024-08-21 11:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.CharField(blank=True, default='guest@example.com', max_length=250),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='phone',
            field=models.CharField(blank=True, default='+49 12 3456789', max_length=30),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='members',
            field=models.JSONField(blank=True, null=True),
        ),
    ]