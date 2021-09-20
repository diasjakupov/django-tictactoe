from game.serializers import GameListSerializer
from game.constants.choices import GAME_STATUS_CHOICES
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import GameInfo

class GameListView(ListAPIView):
    queryset=GameInfo.objects.filter(game_status=GAME_STATUS_CHOICES[0][0], second_player=None)
    serializer_class=GameListSerializer



