from rest_framework import Serializer
from .models import Payement


class PayementSerializer(Serializer.ModelSerializer):
    class Meta:
        model = Payement
        fields = '__all__'