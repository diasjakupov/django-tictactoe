from django.db.models import fields
from rest_framework import serializers
from .models import GameInfo

class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameInfo
        fields='__all__'