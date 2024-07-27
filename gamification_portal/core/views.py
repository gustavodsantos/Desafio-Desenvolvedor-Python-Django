from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Desafio, Corretor, ParticipacaoDesafio


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
