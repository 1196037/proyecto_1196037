from django.shortcuts import render, get_object_or_404
from .models import Persona
from .forms import *


# Create your views here.
def lista_aprendices(request):
	c= Persona.objects.filter()
	return render(request, 'retos/index.html', {'retos': c})


def buscar_ap(request):
	buscar = ""
	if request.method == "POST":#verificar si el formulario esta lleno
		form = busqueda(request.POST)#instancia de la clase 
		if form.is_valid():#si el formulario es valido 
		   buscar = form.cleaned_data['buscar']#limpiar los espacios en blanco 	
		   ap = Persona.objects.filter(nombres=buscar)#query
	else:
		form = busqueda()#formulario vacio
	return render(request, 'retos/index2.html', locals())#renderizacion al html