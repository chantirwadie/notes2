from rest_framework import serializers
from .models import Submit
from devoir.models import Devoir
from devoir.serializers  import DevoirSerializer
class SubmitSerializer(serializers.ModelSerializer):
    devoir = DevoirSerializer()
    class Meta:
        model = Submit
        fields = '__all__'
class SubmitAddSerializer(serializers.ModelSerializer):
    class Meta:
            model = Submit
            fields = '__all__'
    