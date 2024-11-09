from django.urls import path

from gamification_portal.core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('desafios/', views.listar_desafios, name='listar_desafios'),
    path('desafios/<int:id>/', views.detalhes_desafio, name='detalhes_desafio'),
    path('desafios/<int:id>/aceitar/', views.aceitar_desafio, name='aceitar_desafio'),
    path('desafios/atribuir/', views.atribuir_desafio, name='atribuir_desafio'),
    path('usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('usuarios/<int:id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('desafios/cadastrar/', views.cadastrar_desafio, name='cadastrar_desafio'),
    path('desafios/atribuidos/', views.visualizar_desafios_atribuidos, name='visualizar_desafios_atribuidos'),
    path('logged_out/', views.logged_out, name='logged_out'),
]
