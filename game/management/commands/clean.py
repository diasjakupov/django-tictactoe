from django.core.management.base import BaseCommand
from game.models import GameInfo

class Command(BaseCommand):
    help="delete first and second players and their movements"

    def handle(self, *args, **options):
        instance=GameInfo.objects.get(id=10)
        instance.first_player=None
        instance.second_player=None
        instance.movements=""
        instance.save()
