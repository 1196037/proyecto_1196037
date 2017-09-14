from django.shortcuts import render,redirect, get_object_or_404
from .models import Persona, Reto
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.db.models import Q


# Create your views here.
def buscar_ap(request):
	buscar = ""
	if request.method == "POST":#verificar si el formulario esta lleno
		form = busqueda(request.POST)#instancia de la clase 
		if form.is_valid():#si el formulario es valido 
		   buscar = form.cleaned_data['buscar']#limpiar los espacios en blanco 	
		   ap = Persona.objects.filter(Q(nombres__icontains=buscar) | Q(identificacion__icontains=buscar))#query
	else:
		form = busqueda()#formulario vacio
	return render(request, 'retos/index2.html', locals())#renderizacion al html


def aprendices(request):
	p= Persona.objects.all()
	return render(request, 'retos/lista.html' ,{'lista':p})


def editar(request, pk):
		m=get_object_or_404(Persona,pk=pk)
		if request.method=="POST":
			form=PersonaForm(request.POST, request.FILES, instance=m)
			if form.is_valid():
				m=form.save(commit=False)
				m.save()
				return redirect('aprendices')
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
	


def base(request):
	if request.method == "POST":
		form = aprendicesForm(request.POST)
		if form.is_valid():
			aprendiz = form.save(commit=False)
			aprendiz.Hora = 0
			aprendiz.save()
			return redirect(correcto)
	else:
		form = aprendicesForm()
	return render(request, 'retos/base.html', {'form' : form})


def registrar_aprendices(request):
	if request.method == "POST":
		form = aprendicesForm(request.POST)
		if form.is_valid():
			aprendiz = form.save(commit=False)
			aprendiz.Hora = 0
			aprendiz.save()
			return redirect('aprendices')
	else:
		form = aprendicesForm()
	return render(request, 'retos/agregar.html', {'form' : form})


def agregar_categoria(request):
	if request.method == 'POST':
		form = Agregar_Categoria_Forms(request.POST)
		if form.is_valid():
			form.save()
			mensaje = "se almaceno exitosa mente"
			return render(request,'retos/agregar_categoria.html',locals())
	else: 
		form = Agregar_Categoria_Forms()

 	return render(request,'retos/agregar_categoria.html',{'form':form})


def crear_reto(request):
	if request.method == 'POST' :
		form = Crear_Reto_Form(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('crear_reto')
	else:
		form= Crear_Reto_Form()

	return render(request, 'retos/crear_reto.html', {'form': form})


def ranking (request):
	b = Persona.objects.all().order_by("-puntaje")
	return render (request,'retos/ranking.html' , {'lista': b})


def ver_retos(request):
	ver = Reto.objects.all()
	return render(request, 'retos/lista_retos.html', {'m': ver})	


def editar_reto(request, pk):
		editreto=get_object_or_404(Reto,pk=pk)
		if request.method=="POST":
			form=Crear_Reto_Form(request.POST, request.FILES, instance=editreto)
			if form.is_valid():
				editreto=form.save(commit=False)
				editreto.save()
				return redirect('lista_reto')#, pk=m.pk)==podria ir esto....se direciona el nombre del la url
		else:
			z=Crear_Reto_Form(instance=editreto)		
		return render(request, 'retos/editar_reto.html', {'form': z})



def detalle_reto (request, pk):
	ver_detalle_reto= get_object_or_404(Reto, pk=pk)
	return render(request, 'retos/detalle_reto.html', {'detalle': ver_detalle_reto})


def lista_categoria(request):
	cate= Categoria.objects.all()
	return render(request, 'retos/lista_categoria.html', {'categorias': cate})	

def editar_categoria(request, pk):
		editcategoria=get_object_or_404(Categoria,pk=pk)
		if request.method=="POST":
			form=Agregar_Categoria_Forms(request.POST, request.FILES, instance=editcategoria)
			if form.is_valid():
				editcategoria=form.save(commit=False)
				editcategoria.save()
				return redirect('lista_categorias')#, pk=m.pk)==podria ir esto....se direciona el nombre del la url
		else:
			h=Agregar_Categoria_Forms(instance=editcategoria)		
		return render(request, 'retos/editar_categoria.html', {'form': h})		
