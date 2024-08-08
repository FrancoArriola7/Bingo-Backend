from django.contrib import admin
from .models import Musical, Carton, Casilla

class CasillaInline(admin.TabularInline):
    model = Casilla
    extra = 1

class CartonAdmin(admin.ModelAdmin):
    inlines = [CasillaInline]

admin.site.register(Musical)
admin.site.register(Carton, CartonAdmin)
admin.site.register(Casilla)