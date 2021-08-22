from game.constants.choices import GAME_STATUS_CHOICES
from game.models import GameInfo


class GameManager():
    def __init__(self, user) -> None:
        self.user=user
        self.game=None


    def createGameInstance(self):
        try:
            instance=GameInfo.objects.create(first_player=self.user, game_status=GAME_STATUS_CHOICES[0][0])
            self.game=instance
            return True
        except Exception as e:
            print("method createGameInstance" + e)
            return False

    def deleteGameInstance(self, game_id):
        GameInfo.objects.get(pk=game_id).delete()

    def connectToGame(self, game_id):
        try:
            instance=GameInfo.objects.get(pk=game_id)
            if(instance.game_status==GAME_STATUS_CHOICES[0][0]):
                instance.second_player=self.user
                instance.save()
                instance.game_status=GAME_STATUS_CHOICES[1][0]
                self.game=instance
                return True
            else:
                return False
        except Exception as e:
            print("method connectToGame" + e)
            return False

    def makeMove(self, x, y):
        newMove={"user":self.user.id, "x":x, "y":y}
        self.game.movements=f"{self.game.movements}, {newMove}" if self.game.movements!="" else f"{newMove}"
        return self.game.movements