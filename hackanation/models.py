from django.db import models

# Create your models here.
class Prizes(models.Model):
    website_hash = models.CharField(max_length=255,unique=True)
    website = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    category = models.CharField(max_length=200)
    value = models.IntegerField(max_length=10)
    value_description = models.CharField(max_length=1000)

class Projects(models.Model):
    name = models.CharField(max_length=1000)
    region = models.CharField(max_length=400)
    event = models.CharField(max_length=400)
    team_name = models.CharField(max_length=200)
    prizes = models.ManyToManyField(Prizes)
    website_hash = models.CharField(max_length=255,unique=True)
    website = models.CharField(max_length=1000)


