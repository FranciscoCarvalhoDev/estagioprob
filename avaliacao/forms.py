from django.forms import forms, TextInput, SelectMultiple, Select
from django import forms


class AvaliacaoForm(forms.Form):
    data = forms.CharField()
    tipo = forms.CharField()
    nivel = forms.CharField()
    media = forms.CharField()
    periodo = forms.CharField()
    funcionario = forms.CharField()


class CriterioForm(forms.Form):
    descricao = forms.CharField()
    nota = forms.CharField()
    categoria = forms.CharField()
    avaliacao = forms.CharField()




