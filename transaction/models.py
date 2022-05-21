from django.db import models
from payement.models import Payement

# Create your models here.


class Transaction(models.Model):

    payement = models.ForeignKey(Payement, on_delete=models.CASCADE)
    amount = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)