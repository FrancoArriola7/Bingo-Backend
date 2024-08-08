from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MusicalViewSet, CartonViewSet, elegir_musical, actualizar_cartones, resetearJuego

router = DefaultRouter()
router.register(r'musicals', MusicalViewSet)
router.register(r'cartons', CartonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cartons/generar/', CartonViewSet.as_view({'post': 'generar'}), name='carton-generar'),
    path('cartons/<int:pk>/obtener/', CartonViewSet.as_view({'get': 'obtener'}), name='carton-obtener'),
    path('elegir_musical/', elegir_musical, name='elegir_musical'),
    path('actualizar_cartones/', actualizar_cartones, name='actualizar_cartones'),
    path('reset/', resetearJuego, name='resetearJuego')
]