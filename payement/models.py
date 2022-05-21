from django.db import models

# Create your models here.


class Payement(models.Model):

    type = models.CharField(max_length=60, blank=False, null=False)
    amount = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
