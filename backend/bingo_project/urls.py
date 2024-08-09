from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('/api/')

urlpatterns = [
    path('', home_redirect),  # Redirige la raíz a /api/
    path('admin/', admin.site.urls),
    path('api/', include('bingo.urls')),
]
