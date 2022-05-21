from django.db import models
from cProfile import label


# Create your models here.
class Devoir(models.Model):
    sujet = models.CharField(max_length=255, blank=True,null=True)
    description = models.CharField(max_length=255, blank=True,null=True)
    professeur = models.IntegerField(null=True)
    element = models.IntegerField(null=True)
    date_limit = models.CharField(null=True,max_length=255)
    document = models.FileField(upload_to='documents/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
