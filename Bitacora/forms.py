# forms.py
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'lastname', 'position', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class ModeloForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['idModelo', 'Nombre']
    