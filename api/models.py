from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Question(models.Model):
    text = models.TextField()
    clue = models.TextField(default='', blank=True, null=True)
    clue_wait_time = models.IntegerField(default=5)
    round = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=100)
    media = models.FileField(upload_to="questions/", blank=True, null=True)
    points = models.IntegerField(default=10)
    coins = models.IntegerField(default=10)
    ogmedia = models.CharField(max_length=100, default="Movie")
    year = models.IntegerField(default = 2000)
    language = models.CharField(max_length=100, default="Hindi")
    country = models.CharField(max_length=250, default="India")


class User(AbstractUser):
    current_round = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    calc_wait_time_from = models.DateTimeField(blank=True, null=True)
    picture = models.URLField(verbose_name="Avatar of the user: ", default=None, null=True)
    cardTypeA = models.CharField(max_length=10, default="000000000")
    coins_aval = models.IntegerField(default=0)
    show_country = models.BooleanField(default = False) 
    show_media = models.BooleanField(default = False)
    show_language = models.BooleanField(default = False)
    show_year = models.BooleanField(default = False)
    rf_active = models.BooleanField(default = False)
    rf_start_time = models.DateTimeField(blank=True, null=True)

class Meta(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Card(models.Model):
    card_type = models.IntegerField(default = 0)
    card_num = models.IntegerField(default=5)
    card_text = models.CharField(max_length=100)
    card_desc = models.CharField(max_length=500)
    card_coins = models.IntegerField(default=10)

class Update(models.Model):
    update_text = models.CharField(max_length=500)
    time = models.DateTimeField(blank=True, null=True)