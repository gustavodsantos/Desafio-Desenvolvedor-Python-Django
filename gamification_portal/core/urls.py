from django.urls import path
from . import views

urlpatterns = [
    path('desafios/', views.listar_desafios, name='listar_desafios'),
    path('desafios/<int:id>/', views.detalhes_desafio, name='detalhes_desafio'),
    path('desafios/<int:id>/aceitar/', views.aceitar_desafio, name='aceitar_desafio'),
]
