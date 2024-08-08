from django.core.management.base import BaseCommand
from bingo.models import Carton

class Command(BaseCommand):
    help = 'Elimina todos los cartones de la base de datos'

    def handle(self, *args, **kwargs):
        Carton.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Todos los cartones han sido eliminados.'))
