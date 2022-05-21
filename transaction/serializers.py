from rest_framework import Serializer
from .models import Transaction



class TransactionSerializer(Serializer.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'