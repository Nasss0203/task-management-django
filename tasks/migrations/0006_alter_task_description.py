# Generated by Django 3.2.25 on 2025-05-16 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_remove_task_statusid_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
