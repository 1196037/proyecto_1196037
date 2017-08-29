from django import forms
from .models import *

class busqueda(forms.Form):
	buscar = forms.CharField()