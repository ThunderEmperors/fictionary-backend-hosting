# Generated by Django 5.0.6 on 2024-12-19 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_question_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='show_country',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='show_language',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='show_media',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='show_year',
            field=models.BooleanField(default=False),
        ),
    ]
