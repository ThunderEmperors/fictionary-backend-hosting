# Generated by Django 5.0.6 on 2024-12-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.IntegerField(default=0)),
                ('card_num', models.IntegerField(default=5)),
                ('card_text', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='cardTypeA',
            field=models.CharField(default='000000000', max_length=10),
        ),
    ]
