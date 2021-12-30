from django.db import models

# Create your models here.
class Vote(models.Model):
    like = models.IntegerField(default=1)
    deslike = models.IntegerField(default=0)
    total = models.IntegerField(default=1)

    def likes(self):
        self.like += 1
        self.total += 1
    
    def deslikes(self):
        self.deslike += 1
        self.total += 1