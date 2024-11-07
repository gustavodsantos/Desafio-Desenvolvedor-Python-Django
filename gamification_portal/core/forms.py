from django import forms

from .models import Corretor, Desafio


class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ['nome', 'descricao', 'banner', 'regras_pontuacao']

        # Tornar o campo 'banner' não obrigatório
        banner = forms.ImageField(required=False)


class CorretorForm(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = ['user', 'cpf']


class AtribuirDesafioForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    desafio = forms.ModelChoiceField(queryset=Desafio.objects.all())
