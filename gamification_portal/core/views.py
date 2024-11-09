import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from PIL import Image

from .forms import AtribuirDesafioForm, CorretorForm, DesafioForm
from .models import Corretor, Desafio, ParticipacaoDesafio


def home(request):
    return render(request, 'core/home.html')


def logged_out(request):
    return render(request, 'registration/logged_out.html')


def converter_jfif_para_png(diretorio):
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.jfif'):
            caminho_jfif = os.path.join(diretorio, arquivo)
            caminho_png = os.path.join(diretorio, arquivo.replace('.jfif', '.png'))

            # Abrir e converter a imagem
            with Image.open(caminho_jfif) as img:
                img.save(caminho_png, 'PNG')
            print(f'{arquivo} convertido para {caminho_png}')


@login_required
def listar_desafios(request):
    # Diretório onde as imagens JFIF estão localizadas
    diretorio_banners = (
        '/home/gustavo/PycharmProjects/Desafio-Desenvolvedor-Python-Django/docker_desafio/mediafiles/banners'
    )

    # Chama a função para converter as imagens JFIF para PNG
    converter_jfif_para_png(diretorio_banners)

    desafios = Desafio.objects.all()
    return render(request, 'core/listar_desafios.html', {'desafios': desafios})


@login_required
def detalhes_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)
    participacao = ParticipacaoDesafio.objects.filter(corretor__user=request.user, desafio=desafio).first()
    return render(request, 'core/detalhes_desafio.html', {'desafio': desafio, 'participacao': participacao})


@login_required
def aceitar_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)

    # Tenta obter o perfil de corretor do usuário logado
    try:
        corretor = Corretor.objects.get(user=request.user)
    except Corretor.DoesNotExist:
        messages.error(request, 'Você não possui um perfil de corretor e não pode aceitar desafios.')
        return redirect('listar_desafios')  # Redireciona para a lista de desafios, ou outra página de sua escolha

    # Cria ou obtém a participação no desafio
    participacao, created = ParticipacaoDesafio.objects.get_or_create(corretor=corretor, desafio=desafio)
    participacao.aceito = True
    participacao.save()

    messages.success(request, 'Desafio aceito com sucesso!')
    return redirect('listar_desafios')


@login_required
def cadastrar_desafio(request):
    if request.method == 'POST':
        form = DesafioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('Formulário válido, redirecionando...')
            return redirect('listar_desafios')
        else:
            print('Erros no formulário:', form.errors)
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
            return redirect('core:gerenciar_usuarios')
    else:
        form = CorretorForm(instance=corretor)
    return render(request, 'core/editar_usuario.html', {'form': form})


@login_required
def atribuir_desafio(request):
    if request.method == 'POST':
        form = AtribuirDesafioForm(request.POST)
        if form.is_valid():
            try:
                corretor = Corretor.objects.get(cpf=form.cleaned_data['cpf'])
            except Corretor.DoesNotExist:
                form.add_error('cpf', 'Corretor não encontrado.')
                return render(request, 'core/atribuir_desafio.html', {'form': form})

            desafio = form.cleaned_data['desafio']
            ParticipacaoDesafio.objects.create(corretor=corretor, desafio=desafio)
            return redirect('listar_desafios')
    else:
        form = AtribuirDesafioForm()
    return render(request, 'core/atribuir_desafio.html', {'form': form})


@login_required
def visualizar_desafios_atribuidos(request):
    corretor = Corretor.objects.get(user=request.user)
    participacoes = ParticipacaoDesafio.objects.filter(corretor=corretor)
    return render(request, 'core/visualizar_desafios_atribuidos.html', {'participacoes': participacoes})
