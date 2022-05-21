from rest_framework import serializers
from .models import Devoir

class DevoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devoir
        fields = '__all__'
class DevoirAddSerializer(serializers.ModelSerializer):
    class Meta:
            model = Devoir
            fields = '__all__'
    