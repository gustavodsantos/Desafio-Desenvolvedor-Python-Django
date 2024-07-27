from django import forms
from .models import Desafio, Corretor


class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ['nome', 'descricao', 'banner', 'regras_pontuacao']


class CorretorForm(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = ['user', 'cpf']


class AtribuirDesafioForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    desafio = forms.ModelChoiceField(queryset=Desafio.objects.all())
