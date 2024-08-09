from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Musical, Carton, Casilla
from .serializers import MusicalSerializer, CartonSerializer
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random, json


class MusicalViewSet(viewsets.ModelViewSet):
    queryset = Musical.objects.all()
    serializer_class = MusicalSerializer

class CartonViewSet(viewsets.ModelViewSet):
    queryset = Carton.objects.all()
    serializer_class = CartonSerializer

    @action(detail=False, methods=['post'])
    def generar(self, request):
        jugador = request.data.get('jugador')
        if not jugador:
            return Response({'error': 'El nombre del jugador es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            carton = Carton.create_unique_carton(jugador)
            serializer = CartonSerializer(carton)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'No se pudo generar un cartón único.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def obtener(self, request, pk=None):
        carton = get_object_or_404(Carton, pk=pk)
        serializer = CartonSerializer(carton)
        return Response(serializer.data)
    
@csrf_exempt
def elegir_musical(request):
    if request.method == 'POST':
        musicales_no_elegidos = list(Musical.objects.filter(elegido=False))
        if not musicales_no_elegidos:
            return JsonResponse({'status': 'error', 'message': 'No hay musicales disponibles para elegir.'})

        musical = random.choice(musicales_no_elegidos)
        musical.elegido = True
        musical.save()

        # Actualizar casillas correspondientes en los cartones
        casillas = Casilla.objects.filter(musical=musical)
        for casilla in casillas:
            casilla.marcado = True
            casilla.save()

        # Send WebSocket message
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "game_group",
            {
                "type": "musical_selected",
                "musical": musical.nombre,
            }
        )

        return JsonResponse({'status': 'success', 'musical': musical.nombre, 'message': f'{musical.nombre} marcado como elegido y casillas actualizadas.'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

@csrf_exempt
def actualizar_cartones(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        musical_nombre = data.get('musical')
        if not musical_nombre:
            return JsonResponse({'status': 'error', 'message': 'Nombre del musical es requerido.'})

        try:
            musical = Musical.objects.get(nombre=musical_nombre)
        except Musical.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Musical no encontrado.'})

        casillas = Casilla.objects.filter(musical=musical)
        for casilla in casillas:
            casilla.marcado = True
            casilla.save()

        return JsonResponse({'status': 'success', 'message': f'Cartones actualizados para el musical {musical_nombre}.'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

@csrf_exempt
def resetearJuego(request):
    if request.method == 'POST':
        Musical.objects.update(elegido=False)

        # Eliminar todos los cartones y casillas asociadas
        Carton.objects.all().delete()
        
        return JsonResponse({'status': 'success', 'message': 'Todos los estados de los musicales han sido reseteados a False y los cartones han sido eliminados.'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})
