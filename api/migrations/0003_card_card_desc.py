# Generated by Django 5.0.6 on 2024-12-07 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_card_user_cardtypea'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_desc',
            field=models.CharField(default='Basic Card Description', max_length=500),
            preserve_default=False,
        ),
    ]