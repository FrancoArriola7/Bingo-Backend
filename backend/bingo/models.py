import uuid
from django.db import models, IntegrityError
import random

class Musical(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    elegido = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Carton(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jugador = models.CharField(max_length=255)
    musicales = models.ManyToManyField(Musical, through='Casilla')
    combinacion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Cartón de {self.jugador}"

    @classmethod
    def create_unique_carton(cls, jugador):
        musicales = list(Musical.objects.all())
        if len(musicales) < 4:
            raise ValueError("No hay suficientes musicales para generar un cartón único.")

        attempt_count = 0
        while True:
            attempt_count += 1
            selected_musicals = random.sample(musicales, 4)
            sorted_musicals = sorted(selected_musicals, key=lambda m: m.nombre)
            combinacion = ','.join([m.nombre for m in sorted_musicals])
            if not cls.carton_exists(combinacion):
                carton = cls.objects.create(jugador=jugador, combinacion=combinacion)
                for musical in sorted_musicals:
                    Casilla.objects.create(carton=carton, musical=musical)
                print(f'Cartón generado después de {attempt_count} intentos.')
                return carton

    @staticmethod
    def carton_exists(combinacion):
        return Carton.objects.filter(combinacion=combinacion).exists()

class Casilla(models.Model):
    carton = models.ForeignKey(Carton, on_delete=models.CASCADE)
    musical = models.ForeignKey(Musical, on_delete=models.CASCADE)
    marcado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.musical.nombre} en cartón de {self.carton.jugador}"