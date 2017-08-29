from django.shortcuts import render,redirect, get_object_or_404
from .models import Persona
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect



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

def aprendices(request):
	p= Persona.objects.all()
	return render(request, 'retos/lista_aprendiz.html' ,{'lista':p})

def post_new(request):
	if request.method == "POST":
		form = PersonaForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('aprendices')
	else:
		form = PersonaForm()
	return render(request, 'retos/agregar.html', {'form': form})
		# form = RegistroForm()
		# return render(request, 'vistas_html/editar.html', {'form': form})



def editar(request, pk):
		m=get_object_or_404(Persona,pk=pk)
		if request.method=="POST":
			form=PersonaForm(request.POST, request.FILES, instance=m)
			if form.is_valid():
				m=form.save(commit=False)
				m.save()
				return redirect('aprendices')#, pk=m.pk)==podria ir esto....se direciona el nombre del la url
		else:
			r=PersonaForm(instance=m)		
		return render(request, 'retos/editar.html', {'form': r})


def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			formulario = Login_form(request.POST)
			if formulario.is_valid():
				usu = formulario.cleaned_data ['usuario']
				pas = formulario.cleaned_data ['clave']
				usuario = authenticate(username = usu, password = pas)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario o clave incorrecta vuelve a intentarlo"
		formulario = Login_form()
		ctx = {'form':formulario, 'mensaje':mensaje}
		return render(request, 'retos/login.html', ctx)


def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
	
