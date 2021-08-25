from game.constants.choices import GAME_STATUS_CHOICES
from game.models import GameInfo
from game.models import GameMove
import json


class GameManager():
    def __init__(self, user) -> None:
        self.user=user
        self.game=None
        self.sign=None
        self.game_size=3 #TODO make a dynamic size of field


    def createGameInstance(self):
        try:
            instance=GameInfo.objects.create(first_player=self.user, game_status=GAME_STATUS_CHOICES[0][0])
            self.game=instance
            self.sign="X"
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
                self.sign="O"
                return True
            else:
                return False
        except Exception as e:
            print("method connectToGame" + str(e))
            return False

    def makeMove(self, x, y):
        listOfMoves=[]
        newMove=GameMove(self.user.id, self.sign, x, y)
        if self.game.movements!="":
            listOfMoves.append(json.loads(self.game.movements))
        listOfMoves.append(newMove.__dict__)
        self.game.movements=f'[{json.dumps(listOfMoves).replace("[","").replace("]", "")}]'
        isEnded=self._checkTheGameStatus(self.game.movements)
        return self.game.movements, isEnded

    def _checkTheGameStatus(self, movements)->int:
        decoded_moves=json.loads(movements)
        isWon=self._checkForWin([i for i in decoded_moves if i["userId"]==self.user.id])
        if len(decoded_moves)==self.game_size**2:
            return -1
        return int(isWon)

    def _checkForWin(self, movements: list)-> bool:
        listOfCoo=[]
        for i in movements:
            listOfCoo.append([int(i["x"]), int(i["y"])])
        #FIXME later replace this logic with minimax algorithm
        xwin=self._checkLineWin(listOfCoo, 0) #0 is equal to x
        ywin=self._checkLineWin(listOfCoo, 1) #while 1 is equal to y
        dwin=self._checkDiagonalWin(listOfCoo)
        return xwin or ywin or dwin

    def _checkLineWin(self, movements: list, coo: int)->bool:
        cooStorage=[]
        for i in movements:
            cooStorage.append(i[coo])

        neededMoves=[i for i in range(1, self.game_size+1)]
        
        if(cooStorage==neededMoves):
            return True    
            
        return False

    def _checkDiagonalWin(self, movements: list)->bool:
        neededCoo=[[i,i] for i in range(1, self.game_size+1)]
        if neededCoo==movements:
            return True
        return False

        
