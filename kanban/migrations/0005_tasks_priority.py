# Generated by Django 5.1 on 2024-08-31 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0004_remove_tasks_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
