from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import UUIDField
from .constants.choices import GAME_STATUS_CHOICES
# Create your models here.

class GameMove:
    def __init__(self, userId, sign, n) -> None:
        self.userId=userId
        self.sign=sign
        self.n=n

class GameInfo(models.Model):
    code=models.CharField(unique=True, max_length=6, blank=True, null=True)
    name=models.CharField(max_length=255, null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    first_player=models.ForeignKey(User, on_delete=models.PROTECT, 
                                    verbose_name='First player',
                                    related_name='first_player',
                                    null=True
                                    )
    first_player_sign=models.CharField(max_length=1, null=True, blank=True)
    second_player=models.ForeignKey(User, on_delete=models.PROTECT, 
                                    verbose_name='Second player',
                                    related_name='second_player',
                                    null=True
                                    )
    second_player_sign=models.CharField(max_length=1, null=True, blank=True)
    movements=models.TextField(blank=True, default="")
    game_status=models.CharField(verbose_name="Game Status", 
                                choices=GAME_STATUS_CHOICES,
                                max_length=100)

    def __str__(self) -> str:
        return f"Game id: {self.pk}"
