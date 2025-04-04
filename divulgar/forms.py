# divulgar/forms.py
from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['foto', 'nome', 'descricao', 'estado', 'cidade', 'telefone', 'raca', 'tags']
