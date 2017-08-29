from django import forms
from .models import *

class busqueda(forms.Form):
	buscar = forms.CharField()

class PersonaForm(forms.ModelForm):

	class Meta:
		model = Persona
		fields = ('identificacion','nombres','apellidos','ficha', 'puntaje','user',)		