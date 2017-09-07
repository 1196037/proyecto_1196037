from django import forms
from .models import *

class busqueda(forms.Form):
	buscar = forms.CharField()

class PersonaForm(forms.ModelForm):
    class Meta:
	model = Persona
	fields = ('identificacion','nombres','apellidos','ficha', 'puntaje','user',)		


class Login_form(forms.Form):
	usuario = forms.CharField(widget = forms.TextInput())
	clave = forms.CharField(widget = forms.PasswordInput(render_value = False))


class aprendicesForm(forms.ModelForm):
	class Meta:
		model = Persona
		fields = ('identificacion','nombres', 'apellidos','ficha','puntaje','user',)

class Agregar_Categoria_Forms(forms.ModelForm):
	class Meta:
		model= Categoria
		fields=[
			'nombre',
		]
		labels={	
			'nombre' :'Nombre',
		}
		widgets={
			'nombre': forms.TextInput(attrs={'class':'form-control'})
		}

class Crear_Reto_Form (forms.ModelForm):
	class Meta: 
		model = Reto
		fields	 = '__all__'
		
# class ver_reto_Form (forms.ModelForm):
# 	class Meta: 
# 		model = Reto
# 		fields	 = '__all__'

	
