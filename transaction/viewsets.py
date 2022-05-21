from rest_framework import viewsets
from .models import Transaction
from .  import serializers


class CreneauViewset(viewsets.ModelViewSet):
    queryset =Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer