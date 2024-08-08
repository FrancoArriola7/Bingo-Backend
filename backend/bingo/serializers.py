from rest_framework import serializers
from .models import Musical, Carton, Casilla

class MusicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musical
        fields = '__all__'

class CasillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Casilla
        fields = '__all__'

class CartonSerializer(serializers.ModelSerializer):
    casillas = CasillaSerializer(many=True, read_only=True)

    class Meta:
        model = Carton
        fields = '__all__'