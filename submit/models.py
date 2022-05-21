from django.db import models
from cProfile import label
from devoir.models import Devoir


# Create your models here.
class Submit(models.Model): 
    devoir = models.ForeignKey(Devoir,unique=False,related_name="submitdevoir", on_delete=models.CASCADE)
    etudiant = models.IntegerField()
    document = models.FileField(upload_to='documents/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




