# Generated by Django 5.0.6 on 2025-01-11 11:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
