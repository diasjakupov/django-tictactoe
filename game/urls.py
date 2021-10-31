from django.urls import path

from .views import *

urlpatterns = [
    path("", GameListView.as_view()),
    path("create_game_instance", CreateGameView.as_view())
]