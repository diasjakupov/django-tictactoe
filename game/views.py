from rest_framework import permissions, status
from game.serializers import GameListSerializer
from game.constants.choices import GAME_STATUS_CHOICES
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from game.utils.gameManager import GameManager
from .models import GameInfo

class GameListView(ListAPIView):
    queryset=GameInfo.objects.filter(game_status=GAME_STATUS_CHOICES[0][0])
    serializer_class=GameListSerializer


class CreateGameView(APIView):
    permissions=[permissions.IsAuthenticated]

    def post(self, request):
        manager=GameManager(request.user)
        if request.method=="POST":
            name, uid=request.data["name"], request.data["uid"]
            manager.createGameInstance(name, uid)
            return Response({"uid": uid}, status=HTTP_201_CREATED)
        else:
            print("hello3")
            return Response({"uid": None}, status=HTTP_400_BAD_REQUEST)




