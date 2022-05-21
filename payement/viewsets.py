from rest_framework import viewsets
from .models import Payement
from .  import serializers


class CreneauViewset(viewsets.ModelViewSet):
    queryset =Payement.objects.all()
    serializer_class = serializers.PayementSerializer