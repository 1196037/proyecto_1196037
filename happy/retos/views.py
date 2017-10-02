from django.shortcuts import render,redirect, get_object_or_404
from .models import Persona, Reto
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, date
from django.contrib.auth.models import User

# Create your views here.
def buscar_ap(request):
	mensaje = ""
	if request.method == "POST":#verificar si el formulario esta lleno
		form = busqueda(request.POST)#instancia de la clase 
		if form.is_valid():#si el formulario es valido 
		   buscar = form.cleaned_data['buscar']#limpiar los espacios en blanco
		   ap = Persona.objects.filter(Q(nombres__icontains=buscar) | Q(identificacion__icontains=buscar))#query
		   if ap:
			pass
		   else:
			mensaje = "no hay resultado"
	else:	
		form = busqueda()#formulario vacio
	return render(request, 'retos/index2.html', locals())#renderizacion al html


def aprendices(request):
	p= Persona.objects.all()
	return render(request, 'retos/lista.html' ,{'lista':p})


# def editar(request, pk):
# 		persona =get_object_or_404(Persona,pk=pk)
# 		if request.method=="POST":
# 			form =PersonaForm(request.POST, request.FILES, instance=persona)#instancia
# 			if form.is_valid():
# 				m=form.save(commit=False)
# 				m.save()
# 				return redirect('aprendices')
# 		else:
# 			form =PersonaForm(instance=persona)		
# 		return render(request, 'retos/editar.html', {'form': form})


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
	fecha_publicacion = date.today()
	fecha_limite = date.today()
	if request.method == 'POST' :
		form = Crear_Reto_Form(request.POST, request.FILES)
		if form.is_valid():
			# fecha_publicacion = form.cleaned_data ['fecha_publicacion']
			# fecha_limite = form.cleaned_data ['fecha_limite']
			# if fecha_publicacion>fecha_limite:
			# 	mensaje = "la fecha publicacion no puede ser mayor a la fecha limite"

			# else:
			# 	fecha_limite<fecha_publicacion
			# 	mensaje2 = "la fecha limite no puede ser menor a la fehca de publicacion"
				form.save()
				return redirect('lista_reto')  
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

def listar_mis_retos(request):
	lista = Persona_Reto.objects.all().order_by('id')
	conntexto = {'listas':lista}
	return render (request, 'retos/listar_mis_retos.html',conntexto)

def eliminar_reto(request, pk):
		l = Reto.objects.get(pk=pk)
		if request.method == "POST":
			l.delete()
			return redirect('lista_reto')
		return render(request,'retos/eliminar_reto.html',{'l':l})



def lista_sin_c(request):
	l = Persona_Reto.objects.filter(calificacion= None , estado = 'sin calificar' )
	return render(request, 'retos/lista_reto_por_calificar.html' ,{'lc':l})	 

def registrar_aprendices(request):
	if request.method == "POST":
		form_a= RegisterForm(request.POST)
		form_b= aprendicesForm(request.POST, request.FILES, prefix="b")
		if form_b.is_valid() and form_a.is_valid():
			usuario 		= form_a.cleaned_data['username']
			email 			= form_a.cleaned_data['email']
			password_one	= form_a.cleaned_data['password_one']
			password_two 	= form_a.cleaned_data['password_two']			
			u = User.objects.create_user(username = usuario,email = email, password = password_one)
			u.save() #guarda el objeto
			b = form_b.save(commit=False)
			# b.user = user
			b.user= u 
			b.save()
			return redirect('aprendices')
			ctx = {'form_a':form_a, 'form_b':form_b}
	else:
		form_a = RegisterForm()
		form_b = aprendicesForm(prefix = "b")
		ctx = {'form_a':form_a, 'form_b':form_b}
	return render(request, 'retos/agregar_aprendiz.html',locals())


def editar(request, pk):
		mensaje=""
		# formulario_user=""
		form=""
		ry={}
		m=get_object_or_404(Persona,pk=pk)
		usua = User.objects.get(id= m.user.id)
		if request.method=="POST":
			form=PersonaForm(request.POST, request.FILES, instance=m)
			formulario_user = editar_user_form(request.POST, instance = usua)
			if form.is_valid() and formulario_user.is_valid():
				editar_usua = form.save(commit = False)
				editar_usua.save()
				# usua.user.set_password(formulario_user.cleaned_data['clave'])
				formulario_user.save()
				mensaje = "Guardado Satisfactoriamente"
				# CREATE   UPDATE
				# return render(request, 'retos/editar_aprendiz.html',locals())	
				return redirect('aprendices')
			else:
				mensaje=mensaje	
		else:
			form=PersonaForm(instance=m)	
			formulario_user=editar_user_form(instance=usua)
			#ry={'form':r,'formulario_user':y}
		return render(request, 'retos/editar_aprendiz.html',locals())

def lista_retos_calificados(request):
	calificados= Persona_Reto.objects.filter(calificacion= 0 , estado = 'calificado')
	return render(request, 'retos/lista_retos_calificados.html', {'rcalificados': calificados})


def eliminar_ap(request, pk):
	ap = Persona.objects.get(id=pk) # SELECT * FROM Categoria Where id = pk
	ap.delete()
	return redirect('aprendices')
	

def eliminar_categoria(request,pk):
	categoria = Categoria.objects.get(id=pk) # SELECT * FROM Categoria Where id = pk
	lista = Reto.objects.filter( categoria=categoria)
	if (len(lista)==0):
		categoria.delete()
		return redirect('lista_categorias')
	else:
		alerta= "la categoria ya esta destinada"
	return redirect('lista_categorias')		
	