from django import forms

from .models import Corretor, Desafio


class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ['nome', 'descricao', 'banner', 'regras_pontuacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'banner': forms.FileInput(attrs={'class': 'form-control custom-file-input'}),
            'regras_pontuacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Regras de Pontuação'}),
        }


class CorretorForm(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = ['user', 'cpf']


class AtribuirDesafioForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    desafio = forms.ModelChoiceField(queryset=Desafio.objects.all())
