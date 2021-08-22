from django.db import models
from django.contrib.auth.models import User
from .constants.choices import GAME_STATUS_CHOICES
# Create your models here.


class GameInfo(models.Model):
    timestamp=models.DateTimeField(auto_now_add=True)
    first_player=models.ForeignKey(User, on_delete=models.PROTECT, 
                                    verbose_name='First player',
                                    related_name='first_player'
                                    )
    second_player=models.ForeignKey(User, on_delete=models.PROTECT, 
                                    verbose_name='Second player',
                                    related_name='second_player',
                                    null=True
                                    )
    movements=models.TextField(blank=True, default="")
    game_status=models.CharField(verbose_name="Game Status", 
                                choices=GAME_STATUS_CHOICES,
                                max_length=100)

    def __str__(self) -> str:
        return f"Game id: {self.pk}"
