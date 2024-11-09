import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def user():
    # Cria um usuário para ser usado nos testes
    return User.objects.create_user(email='testuser@example.com', password='password')


@pytest.mark.django_db
def test_template_content_for_anonymous_user(client):
    # Testa o conteúdo do template para um usuário não autenticado
    response = client.get(reverse('core:home'))
    assert response.status_code == 200
    assert 'Gamification Portal' in response.content.decode()
    assert reverse('login') in response.content.decode()
    assert reverse('core:listar_desafios') not in response.content.decode()
    assert 'Logout' not in response.content.decode()


@pytest.mark.django_db
def test_template_content_for_authenticated_user(client, user):
    # Autentica o usuário
    client.login(email='testuser@example.com', password='password')

    # Testa o conteúdo do template para um usuário autenticado
    response = client.get(reverse('core:home'))
    assert response.status_code == 200
    assert 'Gamification Portal' in response.content.decode()
    assert reverse('core:listar_desafios') in response.content.decode()
    assert reverse('core:cadastrar_desafio') in response.content.decode()
    assert reverse('admin:index') in response.content.decode()
    assert 'Logout' in response.content.decode()
    assert reverse('login') not in response.content.decode()


@pytest.mark.django_db
def test_csrf_token_present(client):
    # Verifica se o token CSRF está presente
    response = client.get(reverse('core:home'))
    assert 'name="csrf-token"' in response.content.decode()


@pytest.mark.django_db
def test_static_files_links(client):
    # Testa se os arquivos estáticos estão sendo referenciados corretamente
    response = client.get(reverse('core:home'))
    assert 'core/css/core.css' in response.content.decode()
    assert 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' in response.content.decode()
    assert 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js' in response.content.decode()


@pytest.mark.django_db
def test_logout_form_action(client, user):
    # Verifica se o formulário de logout tem a action correta
    client.login(email='testuser@example.com', password='password')
    response = client.get(reverse('core:home'))
    assert f'action="{reverse("logout")}"' in response.content.decode()
