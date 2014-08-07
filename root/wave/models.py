from django.db import models
from django.contrib.auth.models import User

class Summoner(models.Model):
    user = models.OneToOneField(User)

    id = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=128, primary_key=True, unique=True)
    def __unicode__(self):
        return self.user.username

class Game(models.Model):
    id_no = models.IntegerField(default=0, unique=True)

    def __unicode__(self):
        return self.id_no


    # wardPlaced = models.IntegerField(default=0)
    # wardKilled = models.IntegerField(default=0)
    # totalDamageDealtToChampions = models.IntegerField(default=0)
    # totalDamageTaken = models.IntegerField(default=0)
