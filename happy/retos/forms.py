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


	
