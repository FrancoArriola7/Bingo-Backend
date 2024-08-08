from typing import Any
from django.core.management.base import BaseCommand
from bingo.models import Musical

class Command(BaseCommand):
    help = 'Resetea los estados de los musicales a False para poder jugar de vuelta'

    def handle(self,*args,**kwargs):
        Musical.objects.update(elegido=False)
        self.stdout.write(self.style.SUCCESS('Todos los estados de los musicales han sido reseteados a False.'))

