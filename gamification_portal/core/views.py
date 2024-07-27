from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Desafio, Corretor, ParticipacaoDesafio
from .forms import DesafioForm, CorretorForm, AtribuirDesafioForm


def home(request):
    return render(request, 'core/home.html')


@login_required
def listar_desafios(request):
    desafios = Desafio.objects.all()
    return render(request, 'core/listar_desafios.html', {'desafios': desafios})


@login_required
def detalhes_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)
    return render(request, 'core/detalhes_desafio.html', {'desafio': desafio})


@login_required
def aceitar_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)
    corretor = Corretor.objects.get(user=request.user)
    participacao, created = ParticipacaoDesafio.objects.get_or_create(corretor=corretor, desafio=desafio)
    participacao.aceito = True
    participacao.save()
    return redirect('listar_desafios')


@login_required
def cadastrar_desafio(request):
    if request.method == 'POST':
        form = DesafioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_desafios')
    else:
        form = DesafioForm()
    return render(request, 'core/cadastrar_desafio.html', {'form': form})


@login_required
def gerenciar_usuarios(request):
    corretores = Corretor.objects.all()
    return render(request, 'core/gerenciar_usuarios.html', {'corretores': corretores})


@login_required
def editar_usuario(request, id):
    corretor = get_object_or_404(Corretor, id=id)
    if request.method == 'POST':
        form = CorretorForm(request.POST, instance=corretor)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_usuarios')
    else:
        form = CorretorForm(instance=corretor)
    return render(request, 'core/editar_usuario.html', {'form': form})


@login_required
def atribuir_desafio(request):
    if request.method == 'POST':
        form = AtribuirDesafioForm(request.POST)
        if form.is_valid():
            corretor = Corretor.objects.get(cpf=form.cleaned_data['cpf'])
            desafio = form.cleaned_data['desafio']
            ParticipacaoDesafio.objects.create(corretor=corretor, desafio=desafio)
            return redirect('listar_desafios')
    else:
        form = AtribuirDesafioForm()
    return render(request, 'core/atribuir_desafio.html', {'form': form})

# Corretores


@login_required
def visualizar_desafios_atribuidos(request):
    corretor = Corretor.objects.get(user=request.user)
    participacoes = ParticipacaoDesafio.objects.filter(corretor=corretor)
    return render(request, 'core/visualizar_desafios_atribuidos.html', {'participacoes': participacoes})
