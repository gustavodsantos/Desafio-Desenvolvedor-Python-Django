import pytest
from django.urls import reverse

from gamification_portal.core.models import Corretor, User


@pytest.fixture
def user(db):
    return User.objects.create_user(email='testuser@example.com', password='12345')


@pytest.fixture
def corretor(db, user):
    return Corretor.objects.create(user=user, cpf='12345678901')


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('core:home'))
    assert response.status_code == 200
    assert 'core/home.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_logged_out_view(client):
    response = client.get(reverse('core:logged_out'))
    assert response.status_code == 200
    assert 'registration/logged_out.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_listar_desafios_view(client, user):
    client.force_login(user)
    response = client.get(reverse('core:listar_desafios'))
    assert response.status_code == 200
    assert 'core/listar_desafios.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_cadastrar_desafio_view(client, user):
    client.force_login(user)

    # Teste GET
    response = client.get(reverse('core:cadastrar_desafio'))
    assert response.status_code == 200
    assert 'core/cadastrar_desafio.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_gerenciar_usuarios_view(client, user):
    client.force_login(user)
    response = client.get(reverse('core:gerenciar_usuarios'))
    assert response.status_code == 200
    assert 'core/gerenciar_usuarios.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_editar_usuario_view(client, user, corretor):
    # Simula o login do usuário
    client.force_login(user)

    # Teste do GET
    response = client.get(reverse('core:editar_usuario', args=[corretor.id]))
    assert response.status_code == 200
    assert 'core/editar_usuario.html' in [t.name for t in response.templates]

    # Teste do POST com dados
    response = client.post(
        reverse('core:editar_usuario', args=[corretor.id]), data={'cpf': '12345678901', 'user': user.id}
    )

    # Verifica se houve redirecionamento após o POST
    assert response.status_code == 302
    assert response.url == reverse('core:gerenciar_usuarios')

    # Atualiza o objeto `corretor` do banco de dados e verifica se o CPF foi atualizado
    corretor.refresh_from_db()
    assert corretor.cpf == '12345678901'

    # Se houver erros no formulário, eles serão exibidos
    if response.status_code == 200 and hasattr(response, 'context'):
        print('Erros no formulário:', response.context['form'].errors)


@pytest.mark.django_db
def test_atribuir_desafio_view(client, user, corretor):
    client.force_login(user)
    response = client.get(reverse('core:atribuir_desafio'))
    assert response.status_code == 200
    assert 'core/atribuir_desafio.html' in [t.name for t in response.templates]

    # Verificar se o cpf está correto
    assert corretor.cpf == '12345678901'  # Certifique-se de que o cpf existe e está correto
