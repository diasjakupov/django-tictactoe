from game.constants.choices import GAME_STATUS_CHOICES
from game.constants.game_signs import GameSigns
from game.models import GameInfo
from game.models import GameMove
import uuid
import json
import math
import random


class GameManager():
    def __init__(self, user) -> None:
        self.user=user
        self.game=None
        self.sign=None
        self.game_size=9 #TODO make a dynamic size of field
        self.cooSystem=self._createTheCooSystem()
        self.lineWin=[i for i in range(1, int(math.sqrt(self.game_size))+1)]
        self.diagonalWin=[[i,i] for i in range(1, int(math.sqrt(self.game_size))+1)]





    def createGameInstance(self, name):
        try:
            first_sign = GameSigns.x if random.random.randint(1, 2)==1 else GameSigns.o
            second_sign= GameSigns.o if first_sign==GameSigns.x else GameSigns.x
            uid=str(uuid.uuid4())[:6]
            instance=GameInfo.objects.create(game_status=GAME_STATUS_CHOICES[0][0],
                                            code=uid,
                                            name=name,
                                            first_player_sign=first_sign,
                                            second_player_sign=second_sign)
            self.game=instance
            return True
        except Exception as e:
            print("method createGameInstance" + e)
            return False

    def deleteGameInstance(self, game_id: int):
        GameInfo.objects.get(pk=game_id).delete()

    def connectToGame(self, game_uid: str):
        try:
            instance=GameInfo.objects.get(code=game_uid)
            if(instance.game_status==GAME_STATUS_CHOICES[0][0]):
                if instance.first_player==None:
                    print("CONNECT FIRST PLAYER", self.user)
                    instance.first_player=self.user
                    self.sign=instance.first_player_sign
                    self._connectPlayer(instance)
                else:
                    print("CONNECT SECOND PLAYER", self.user)
                    instance.second_player=self.user
                    self._connectPlayer(instance)
                    self.sign=instance.second_player_sign
                    #instance.game_status=GAME_STATUS_CHOICES[1][0]
                return True
            else:
                return False
        except Exception as e:
            print("method connectToGame" + str(e))
            return False

    def makeMove(self, n:str):
        self.game=GameInfo.objects.get(id=self.game.id)
        listOfMoves=[]
        newMove=GameMove(self.user.id, self.sign, n) #create new move by its count
        if self.game.movements!="":
            #add previous list
            listOfMoves.append(json.loads(self.game.movements))
        listOfMoves.append(newMove.__dict__) #add new move
        self.game.movements=f'[{json.dumps(listOfMoves).replace("[","").replace("]", "")}]' #save new list of moves
        isEnded=self._checkTheGameStatus(self.game.movements) #checking game status (either it is win or draw)
        self.game.save()
        return self.game.movements, isEnded

    def _checkTheGameStatus(self, movements)->int:
        decoded_moves=json.loads(movements)
        isWon=self._checkForWin([i for i in decoded_moves if i["userId"]==self.user.id])
        if len(decoded_moves)==self.game_size**2:
            return -1 #draw
        return int(isWon) #0 is not ended 1 is win

    def _checkForWin(self, movements: list)-> bool:
        listOfCoo=[]
        for i in movements:
            needCoo=self.cooSystem[self._binarySearch(int(i["n"]))]
            listOfCoo.append(needCoo)
        #FIXME later replace this logic with minimax algorithm
        xwin=self._checkLineWin(listOfCoo, "x") 
        ywin=self._checkLineWin(listOfCoo, "y") 
        dwin=self._checkDiagonalWin(listOfCoo)
        return xwin or ywin or dwin

    def _checkLineWin(self, movements: list, coo: str)->bool:
        cooStorage=[]
        
        for i in movements:
            #create an array of coordinates selected by given coo
            cooStorage.append(i[coo])

        #comparing made coordinates and needed coo to win
        cooStorage.sort()
        if(cooStorage==self.lineWin):
            return True    
            
        return False

    def _checkDiagonalWin(self, movements: list)->bool:
        cooStorage=[]
        for i in movements:
            cooStorage.append([i["x"], i["y"]])
        if self.diagonalWin==movements:
            return True
        return False

    def _createTheCooSystem(self)->list:
        cooSystem=[]
        columnRange=int(math.sqrt(self.game_size))
        yCoo=1
        n=1
        for i in range(1, self.game_size+1, columnRange):
            for x in range(1, columnRange+1):
                cooSystem.append({"x":x, "y":yCoo, "n":n})
                n+=1
            yCoo+=1
        return cooSystem

    def _connectPlayer(self,instance):
        instance.save()
        self.game=instance

    def _binarySearch(self, n: int):
        mid=len(self.cooSystem)//2
        left=0
        right=len(self.cooSystem)
        while left<right:
            if self.cooSystem[mid]["n"]==n:
                return mid
            elif self.cooSystem[mid]["n"]>n:
                right=mid
                mid=(right+left)//2
            elif self.cooSystem[mid]["n"]<n:
                left=mid
                mid=(right+left)//2
        return -1

