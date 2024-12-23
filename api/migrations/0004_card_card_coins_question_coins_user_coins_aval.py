# Generated by Django 5.0.6 on 2024-12-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_card_card_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_coins',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='question',
            name='coins',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='user',
            name='coins_aval',
            field=models.IntegerField(default=0),
        ),
    ]
