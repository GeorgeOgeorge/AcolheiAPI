from django.db import models

from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Preceptor(AbstractUser):
    ocupacao = models.CharField(max_length=255)
    avatar = models.URLField(null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'preceptor'
        verbose_name_plural = 'preceptores'

    def __str__(self):
        return f'{self.username}'

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class ElementoComunicativo(models.Model):
    ativo = models.BooleanField(default=True)
    texto = models.CharField(max_length=255)
    figura = models.URLField()
    libras = models.URLField()
    audioDescricao = models.URLField()
    data = models.DateTimeField(auto_now_add=True)
    tipo = models.BooleanField()

    preceptor = models.ForeignKey(
        Preceptor,
        related_name='elemento_preceptor',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'elemento'
        verbose_name_plural = 'elemento'

    def __str__(self):
        return f'{self.texto}'


class Card(models.Model):
    ativo = models.BooleanField(default=True)
    data = models.DateTimeField(auto_now_add=True)

    titulo = models.ForeignKey(
        ElementoComunicativo,
        null=True,
        related_name='card_titulo_elemento', 
        on_delete=models.DO_NOTHING
    )

    descricao = models.ForeignKey(
        ElementoComunicativo,
        null=True,
        related_name='card_descricao_elemento',
        on_delete=models.DO_NOTHING
    )

    opcoes = models.ManyToManyField(
        ElementoComunicativo,
        related_name='card_opcao'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'card'
        verbose_name_plural = 'cards'
        

class Roteiro(models.Model):
    ativo = models.BooleanField(default=True)
    data = models.DateTimeField(auto_now_add=True)

    titulo = models.ForeignKey(
        ElementoComunicativo,
        related_name='roteiro_titulo_elemento',
        null=True,
        on_delete=models.DO_NOTHING
    )

    descricao = models.ForeignKey(
        ElementoComunicativo,
        related_name='roteiro_descricao_elemento',
        null=True,
        on_delete=models.DO_NOTHING
    )

    cards = models.ManyToManyField(
        Card,
        related_name='roteiro_cards'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'roteiro'
        verbose_name_plural = 'roteiros'


class Paciente(models.Model):
    ativo = models.BooleanField(default=True)
    nome = models.CharField(blank=False, max_length=255)

    class Meta:
        ordering = ['id']
        verbose_name = 'paciente'
        verbose_name_plural = 'pacientes'

    def __str__(self):
        return f'{self.nome}'


class Atendimento(models.Model):
    ativo = models.BooleanField(default=True)
    texto = models.CharField(blank=False, max_length=255)
    data = models.DateTimeField(auto_now_add=True)

    paciente = models.ManyToManyField(Paciente)

    card = models.ManyToManyField(Card)

    opcao = models.ManyToManyField(
        ElementoComunicativo,
        related_name='atendimento_opcao'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'atendimento'
        verbose_name_plural = 'atendimento'
