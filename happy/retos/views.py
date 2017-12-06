from django.shortcuts import render,redirect, get_object_or_404
from .models import *
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
	if request.method == "POST":#_ificar si el formulario esta lleno
		form = busqueda(request.POST)#instancia de la clase 
		if form.is_valid():#si el formulario es valido 
		   buscar = form.cleaned_data['buscar']#obtener el texto en el campo
		   ap = Persona.objects.filter(Q(nombres__icontains=buscar) | Q(identificacion__icontains=buscar))#query
		   if ap:
			pass
		   else:
			mensaje = "no hay resultado"
	else:   
		form = busqueda()#formulario vacio
	return render(request, 'retos/index2.html', locals())#renderizacion al html


def aprendices(request):
	p= Persona.objects.filter(user__is_active = True, user__is_staff = False)
	return render(request, 'retos/lista.html' ,{'lista':p})

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return redirect('lista_reto')
	else:
		if request.method == "POST":
			formulario = Login_form(request.POST)
			if formulario.is_valid():
				usu = formulario.cleaned_data ['usuario']
				pas = formulario.cleaned_data ['clave']
				usuario = authenticate(username = usu, password = pas)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return redirect('lista_reto')
				else:
					mensaje = "usuario o clave incorrecta vuelve a intentarlo"
		formulario = Login_form()
		ctx = {'form':formulario, 'mensaje':mensaje}
		return render(request, 'retos/login.html', ctx)


def logout_view(request):
	logout(request)
	return redirect('/')
	


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

	return render(request,'retos/agregar_categoria.html',locals())

# mensaje = "INFO 001 - Creacion de un reto"
# mensaje = "WARN 001 - Para guardar debe ingresar ....."
# mensaje = "ERRO 001 - Nose pudo Guardar"
# mensaje = "SUCC 001 - Guardado Sqatisfac...."

def crear_reto(request):
	if request.method == 'POST' :
		form = Crear_Reto_Form(request.POST, request.FILES)
		if form.is_valid():
				f=form.save(commit=False)
				f.autor = str(request.user.id)
				dif = form.cleaned_data ['dificultad']
				puntos = form.cleaned_data ['puntos_maximos']
				if dif  == 'basico':
					if puntos > 0 and puntos <= 30:
						f.save()
					else:
						mensaje = "los puntos no pueden ser menores a 0 ni mayores a 30 para la dificultad de basico"
				if dif == 'medio':
					if puntos > 31 and puntos <=70:
						f.save()
					else:
						mensaje = "los puntos no pueden ser menores a 31 ni mayores a 70 para la dificultad de medio"
				if dif == 'dificil':
					if puntos>71 and puntos==100:
						f.save()
					else:
						mensaje = "los puntos no pueden ser menores a 71 ni mayores a 100 para la dificultad de dificil"
				else:
					mensaje = "se guardo correcta mente"
				return render(request, 'retos/crear_reto.html', locals())
	else:
		form= Crear_Reto_Form()
	return render(request, 'retos/crear_reto.html', locals())


def ranking (request):
	b = Persona.objects.filter(user__is_active = True, user__is_staff = False).order_by("-puntaje")
	return render (request,'retos/ranking.html' , {'lista': b})


def ver_retos(request):
	a = Persona.objects.get(user=request.user)
	x = Persona_Reto.objects.filter(persona=a)
	# print "xxxxxxxxxxxx"
	# print x
	# print request.user
	# print "xxxxxxxxxxxx"
	ver = Reto.objects.exclude(id__in=[i.reto.id for i in x])
	return render(request, 'retos/lista_retos.html', {'m': ver})



def editar_reto(request, pk):
		editreto=get_object_or_404(Reto,pk=pk)
		if request.method=="POST":
			form=Crear_Reto_Form(request.POST, request.FILES, instance=editreto)
			if form.is_valid():
				editreto=form.save(commit=False)
				editreto.save()
				return redirect('lista_reto')
		else:
			z=Crear_Reto_Form(instance=editreto)        
		return render(request, 'retos/editar_reto.html', {'form': z})



def detalle_reto (request, pk):
	ver_detalle_reto= get_object_or_404(Reto, pk=pk)
	relacion=Persona_Reto.objects.filter(reto=pk).order_by('-calificacion')[:5]
	return render(request, 'retos/detalle_reto.html', {'detalle': ver_detalle_reto , 'rela':relacion})



def lista_categoria(request):
	lista=[]
	cate= Categoria.objects.all()
	for c in cate:
		retos= Reto.objects.filter(categoria=c.id)
		if(len(retos)>0):
			lista.append(True)  
		else:
			lista.append(False)
	lista3=zip(cate,lista)
	print(lista3)
	return render(request, 'retos/lista_categoria.html', {'cate':cate, 'lista':lista, 'lista3':lista3}) 

def editar_categoria(request, pk):
	mensaje=""
	categoria=Categoria.objects.get(id=pk)
	if request.method=='POST':
		form=Agregar_Categoria_Forms(request.POST, instance=categoria)
		if form.is_valid(): 
			form.save()
			mensaje="se ha Guardado exitosamente"
		return  render( request, 'retos/editar_categoria.html', {'form':form , 'mensaje':mensaje}) 
		#return redirect('lista_categorias')
	else: 
		form=Agregar_Categoria_Forms(instance=categoria)
	return  render( request, 'retos/editar_categoria.html', {'form':form})      


def eliminar_reto(request, pk):
		l = Reto.objects.get(pk=pk)
		l.delete()
		return redirect('lista_reto')
			
def lista_sin_c(request):
	c = User.objects.get(id=request.user.id)
	p = Reto.objects.filter(autor=str(c.id))
	l = Persona_Reto.objects.filter(reto__in=[i.id for i in p], estado = 'sin calificar' )
	return render(request, 'retos/lista_reto_por_calificar.html' ,locals())  

def registrar_aprendices(request):
	if request.method == "POST":
		form_a= RegisterForm(request.POST)
		form_b= aprendicesForm(request.POST, request.FILES, prefix="b")
		if form_b.is_valid() and form_a.is_valid():
			usuario         = form_a.cleaned_data['username']
			# email             = form_a.cleaned_data['email']
			password_one    = form_a.cleaned_data['password_one']
			password_two    = form_a.cleaned_data['password_two']           
			u = User.objects.create_user(username = usuario,password = password_one)#email = email, 
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
	z = User.objects.get(id=request.user.id)
	o = Reto.objects.filter(autor=str(z.id))
	calificados= Persona_Reto.objects.filter(reto__in=[i.id for i in o], estado = 'calificado')
	return render(request, 'retos/lista_retos_calificados.html', {'rcalificados': calificados})


def eliminar_ap(request, pk):
	ap = Persona.objects.get(id=pk)
	ap.delete()
	return redirect('aprendices')
	

def eliminar_categoria(request,pk):
	categoria = Categoria.objects.get(id=pk) # SELECT * FROM Categoria Where id = pk
	lista = Reto.objects.filter(categoria=categoria)
	if (len(lista)==0):
		categoria.delete()
		return redirect('lista_categorias')
	else:
		alerta= "la categoria ya esta destinada"
	return redirect('lista_categorias')



def calificar_reto(request, pk):
	cal = get_object_or_404(Persona_Reto, pk=pk)
	per = Persona.objects.get(pk=cal.persona.id)
	if request.method == 'POST' :
		calform = persona_reto(request.POST , instance = cal)
		if calform.is_valid():
			x = calform.cleaned_data['calificacion']
			if  x<0 or x>100:
				mensaje = "la calificacion no debe mayor a cien ni menor a 0"
			else:
				cal.calificacion=x
				cal.estado='calificado'
				cal.save()
				mensaje = "se guardo correcta mente!"
				# print per.puntaje
				per.puntaje = per.puntaje+x
				per.save()
				return render(request, 'retos/calificar_reto.html', locals())			
	else:
		calform= persona_reto(instance = cal)
	#dic = {'form': calform, 'calificacion': cal}
	#return render(request, 'retos/calificar_reto.html', dic)
	return render(request, 'retos/calificar_reto.html', locals())

def solucionar_reto_i(request, pk):
	r = get_object_or_404(Reto, pk=pk)
	x = Persona.objects.get(user=request.user)
	if request.method == 'POST' :
		form = solucion_reto_i(request.POST , request.FILES)
		if form.is_valid():
			sol = form.save(commit=False)
			sol.reto = r
			sol.persona = x
			sol.estado = "sin calificar"
			sol.save()
			return redirect('lista_reto')
	else:
		form = solucion_reto_i()
		return render(request, 'retos/solucionar_reto_i.html', locals())

def lista_instructor(request):
	pers = Persona.objects.filter(user__is_staff = True)
	return render(request, 'retos/lista_instructores.html', {'personas': pers}) 

def registrar_instructor(request):
	if request.method == "POST":
		form_x= RegisterForm(request.POST)
		form_i= instructorForm(request.POST, request.FILES)
		if form_x.is_valid() and form_i.is_valid():
			usuario         = form_x.cleaned_data['username']
			# email             = form_x.cleaned_data['email']
			password_one    = form_x.cleaned_data['password_one']
			password_two    = form_x.cleaned_data['password_two']           
			u = User.objects.create_user(username = usuario, password = password_one,is_staff=True)#email = email,
			u.save() #guarda el objeto
			persona = form_i.save(commit=False)
			#b.user = user
			persona.user= u 
			persona.save()
			return redirect('lista_instructores')
			#ctx = {'form_x':form_x, 'form_y':form_y}
	else:
		form_x = RegisterForm()
		form_i = instructorForm()
		ctx = {'form_x':form_x, 'form_i':form_i}
	return render(request, 'retos/agregar_instructor.html',locals())

def editar_instructor(request, pk):
		mensaje=""
		# formulario_user=""
		form=""
		ry={}
		m=get_object_or_404(Persona,pk=pk , user__is_staff=True)
		usua = User.objects.get(id= m.user.id)
		if request.method=="POST":
			form=instructorForm(request.POST, request.FILES, instance=m)
			formulario_user = editar_user_form(request.POST, instance = usua)
			if form.is_valid() and formulario_user.is_valid():
				editar_usua = form.save(commit = False)
				editar_usua.save()
				# usua.user.set_password(formulario_user.cleaned_data['clave'])
				formulario_user.save()
				mensaje = "Guardado Satisfactoriamente"
				# CREATE   UPDATE
				# return render(request, 'retos/editar_aprendiz.html',locals()) 
				return redirect('lista_instructores')
			else:
				mensaje=mensaje 
		else:
			form=instructorForm(instance=m) 
			formulario_user=editar_user_form(instance=usua)
			#ry={'form':r,'formulario_user':y}
		return render(request, 'retos/editar_instructor.html',locals())


def eliminar_instructor(request, pk):
	ap = Persona.objects.get(id=pk) # SELECT * FROM Categoria Where id = pk
	ap.delete()
	return redirect('lista_instructors')

def lista_mis_retos(request):
	if request.user.is_staff and request.user.is_active:
		mis_retos_ins = Reto.objects.filter(autor=str(request.user.id))
		# print "xxxxxxxxxxxxxxxxxxxxxxx"
		# print mis_retos_ins
		# print "xxxxxxxxxxxxxxxxxxxxxxx"
		return render(request, 'retos/mis_retos_instructor.html',{'instructor':mis_retos_ins })
		# print Persona.objects.get(user = request.user.id).id  
	elif request.user.is_active:
		mis_retos_apr = Persona_Reto.objects.filter(persona__user = request.user.id)
		# print "xxxxxxxxxxxxxxxxxxxxxxx"
		# print mis_retos_apr, mis_retos_ins
		# print "xxxxxxxxxxxxxxxxxxxxxxx"
	else:
		pass
	return render(request, 'retos/lista_mis_retos.html',{'aprendiz':mis_retos_apr}) 

def inhabilitar_user(request, pk):
	pers = Persona.objects.get(pk=pk)
	#inhabilitar_usuario=User.objects.get(pk=pk)
	if pers.user.is_active:
		pers.user.is_active=False
		pers.user.save()
		return redirect('buscar')
	else:
		pers.user.is_active=True
		pers.user.save()
	return redirect('buscar')


def vista_principal(request):
	return render(request, 'retos/inicio.html', locals())

def ranking_aprendices_retos_mas_realizados(request):
	lista = []
	lista2 = []
	contador = 0
	x= Persona.objects.all()
	l = Persona_Reto.objects.all()
	for i in x:
		for c in l:
			if i == c.persona:
				contador = contador + 1
		if contador!=0:
			lista.append(contador)
			lista2.append(i)
		contador = 0
	l3=zip(lista,lista2)
	print(l3)
	return render (request,'retos/ranking_aprendices_retos_mas_realizados.html' , locals())	
