from django.db import models
from django.contrib.auth.models import User


class Desafio(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    banner = models.ImageField(upload_to='banners/')
    regras_pontuacao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Corretor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    desafios = models.ManyToManyField(Desafio, through='ParticipacaoDesafio')

    def __str__(self):
        return self.user.username


class ParticipacaoDesafio(models.Model):
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE)
    aceito = models.BooleanField(default=False)
    pontuacao = models.IntegerField(default=0)
    posicao = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.corretor} - {self.desafio}'
