from django.core.management.base import BaseCommand
from bingo.models import Musical

class Command(BaseCommand):
    help = 'Popula la base de datos con musicales predefinidos'

    def handle(self, *args, **kwargs):
        musicals = [
            "The Greatest Showman", "Mamma Mía", "Hairspray", "Heathers", "Camp Rock",
            "La La Land", "Aladdin", "Moulin Rouge", "Teen Beach", "School of Rock",
            "High School Musical", "Matilda", "Descendientes", "Glee"
        ]

        for musical in musicals:
            Musical.objects.get_or_create(nombre=musical)

        self.stdout.write(self.style.SUCCESS('Musicales agregados a la base de datos'))
