# Generated by Django 5.0.6 on 2024-12-19 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_question_language_question_ogmedia_question_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='country',
            field=models.CharField(default='India', max_length=250),
        ),
    ]