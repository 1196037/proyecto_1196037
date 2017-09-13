from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Los modelos  estan listos.
NIVELES = (
		('basico','Basico'),
		('medio','Medio'),
		('dificil','Dificil'),
	)
TIPO = (
		('individual','Individual'),
		('grupal','Grupal'),
	)
ESTADO = (
	     ('activo','Activo'),
	     ('incativo','Inactivo'),
	)
class Categoria (models.Model):
	nombre 			= models.CharField(max_length = 50, unique = True)

	def __unicode__ (self):
		return self.nombre 

class Reto (models.Model):
	descripcion			= models.CharField(max_length = 5000)
	fecha_creacion		= models.DateTimeField(auto_now_add = True)
	fecha_publicacion	= models.DateTimeField()
	fecha_limite		= models.DateTimeField()
	tipo 				= models.CharField(max_length = 50, choices = TIPO)
	dificultad			= models.CharField(max_length = 50, choices = NIVELES)
	archivo 			= models.FileField(upload_to = 'retos')
	categoria			= models.ForeignKey(Categoria)
	estado              = models.CharField(max_length = 50, choices = ESTADO)
	like                = models.IntegerField()
	dis_like            = models.IntegerField()

	def __unicode__ (self):
		return self.descripcion

class Persona (models.Model):
	identificacion 	= models.CharField(max_length = 50 , unique = True)
	nombres		 	= models.CharField(max_length = 256)
	apellidos	 	= models.CharField(max_length = 256)
	ficha		 	= models.CharField(max_length = 30)
	puntaje		 	= models.IntegerField()
	user 			= models.OneToOneField(User)

	def __unicode__ (self):
		return self.nombres

class Persona_Reto (models.Model):
	persona			= models.ForeignKey(Persona)
	reto			= models.ForeignKey(Reto)
	fecha_respuesta	= models.DateTimeField(auto_now_add=True)
	calificacion 	= models.IntegerField()
	nombre_grupo 	= models.CharField(max_length = 50)
	archivo 		= models.FileField(upload_to = 'respuestas')

	def __unicode__ (self):
		return self.nombre_grupo
