import os
from io import BytesIO

import pytest
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image

from gamification_portal.core.models import Corretor, Desafio, ParticipacaoDesafio, User


def generate_test_image():
    image = Image.new('RGB', (100, 100), color='white')
    image_file = BytesIO()
    image.save(image_file, 'jpeg')
    image_file.seek(0)
    return SimpleUploadedFile(name='banner.jpg', content=image_file.read(), content_type='image/jpeg')


@pytest.fixture
def user(db):
    return User.objects.create_user(email='testuser@example.com', password='12345')


@pytest.fixture
def corretor(db, user):
    return Corretor.objects.create(user=user, cpf='12345678901')


@pytest.fixture
def desafio(db):
    # Crie o diretório de banners, se não existir
    media_dir = settings.MEDIA_ROOT / 'banners'
    os.makedirs(media_dir, exist_ok=True)

    # Caminho completo para o arquivo dummy
    dummy_image_path = media_dir / 'dummy_image.jpg'

    # Crie um arquivo de imagem dummy (com conteúdo básico de uma imagem PNG, por exemplo)
    with open(dummy_image_path, 'wb') as img_file:
        img_file.write(
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\xdb\xa5\xa5\xd6\x00\x00\x00\x01IDAT8\x8d'
        )

    # Crie o objeto Desafio com o arquivo de imagem
    with open(dummy_image_path, 'rb') as img_file:
        desafio = Desafio.objects.create(
            nome='Desafio Teste',
            descricao='Descrição do Desafio',
            banner=File(img_file, name='dummy_image.jpg'),
            regras_pontuacao='Regras do Desafio',
        )

    return desafio


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'core/home.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_logged_out_view(client):
    response = client.get(reverse('logged_out'))
    assert response.status_code == 200
    assert 'registration/logged_out.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_listar_desafios_view(client, user, desafio):
    client.force_login(user)
    response = client.get(reverse('listar_desafios'))
    assert response.status_code == 200
    assert 'core/listar_desafios.html' in [t.name for t in response.templates]
    assert desafio in response.context['desafios']


@pytest.mark.django_db
def test_detalhes_desafio_view(client, user, corretor, desafio):
    ParticipacaoDesafio.objects.create(corretor=corretor, desafio=desafio, aceito=True)
    client.force_login(user)
    response = client.get(reverse('detalhes_desafio', args=[desafio.id]))
    assert response.status_code == 200
    assert 'core/detalhes_desafio.html' in [t.name for t in response.templates]
    assert response.context['desafio'] == desafio


@pytest.mark.django_db
def test_aceitar_desafio_view(client, user, corretor, desafio):
    client.force_login(user)
    response = client.post(reverse('aceitar_desafio', args=[desafio.id]))
    assert response.status_code == 302
    assert response.url == reverse('listar_desafios')
    participacao = ParticipacaoDesafio.objects.get(corretor=corretor, desafio=desafio)
    assert participacao.aceito is True


@pytest.mark.django_db
def test_cadastrar_desafio_view(client, user):
    client.force_login(user)

    # Teste GET
    response = client.get(reverse('cadastrar_desafio'))
    assert response.status_code == 200
    assert 'core/cadastrar_desafio.html' in [t.name for t in response.templates]

    image = generate_test_image()

    # Teste POST com todos os dados necessários
    response = client.post(
        reverse('cadastrar_desafio'),
        data={
            'nome': 'Novo Desafio',
            'descricao': 'Descrição do Novo Desafio',
            'banner': image,
            'regras_pontuacao': 'Regras de pontuação para o desafio',
        },
    )

    # Espera-se que o formulário seja redirecionado após o sucesso
    assert response.status_code == 302
    assert response.url == reverse('listar_desafios')  # Redirecionamento esperado


@pytest.mark.django_db
def test_gerenciar_usuarios_view(client, user):
    client.force_login(user)
    response = client.get(reverse('gerenciar_usuarios'))
    assert response.status_code == 200
    assert 'core/gerenciar_usuarios.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_editar_usuario_view(client, user, corretor):
    client.force_login(user)
    response = client.get(reverse('editar_usuario', args=[corretor.id]))
    assert response.status_code == 200
    assert 'core/editar_usuario.html' in [t.name for t in response.templates]

    # Teste do POST
    response = client.post(reverse('editar_usuario', args=[corretor.id]), data={'cpf': '12345678901', 'user': user.id})

    if response.status_code == 200 and hasattr(response, 'context'):
        print('Erros no formulário:', response.context['form'].errors)
    assert response.status_code == 302
    assert response.url == reverse('gerenciar_usuarios')

    # Atualiza o objeto `corretor` do banco de dados e verifica se o CPF foi atualizado
    corretor.refresh_from_db()
    assert corretor.cpf == '12345678901'


@pytest.mark.django_db
def test_atribuir_desafio_view(client, user, corretor, desafio):
    client.force_login(user)
    response = client.get(reverse('atribuir_desafio'))
    assert response.status_code == 200
    assert 'core/atribuir_desafio.html' in [t.name for t in response.templates]

    # Verificar se o cpf está correto
    assert corretor.cpf == '12345678901'  # Certifique-se de que o cpf existe e está correto

    # Teste do POST
    response = client.post(reverse('atribuir_desafio'), data={'cpf': corretor.cpf, 'desafio': desafio.id})

    if response.status_code == 200 and hasattr(response, 'context'):
        print('Erros no formulário:', response.context['form'].errors)

    assert response.status_code == 302
    assert response.url == reverse('listar_desafios')


@pytest.mark.django_db
def test_visualizar_desafios_atribuidos_view(client, user, corretor, desafio):
    ParticipacaoDesafio.objects.create(corretor=corretor, desafio=desafio)
    client.force_login(user)
    response = client.get(reverse('visualizar_desafios_atribuidos'))
    assert response.status_code == 200
    assert 'core/visualizar_desafios_atribuidos.html' in [t.name for t in response.templates]
    assert desafio in [p.desafio for p in response.context['participacoes']]
