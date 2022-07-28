from rest_framework import serializers

from .service import CardService, ElementoComunicativoService
from .models import Atendimento, Card, Paciente, Preceptor, Roteiro, ElementoComunicativo
from django.core import serializers as sr

from .utils import checkresult

class AutenticacaoSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    email = serializers.EmailField()
    senha = serializers.CharField()


class PreceptorSerializer(serializers.ModelSerializer):

    elementos_comunicativos = serializers.SerializerMethodField()

    class Meta:
        model = Preceptor
        fields = [
            'id',
            'ocupacao',
            'username',
            'avatar',
            'email',
            'password',
            'elementos_comunicativos'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_elementos_comunicativos(self, obj):
        elementos_preceptor = []
        elementos = ElementoComunicativo.objects.filter(preceptor_id=obj.id)
        for elemento in elementos:
            elementos_preceptor.append(f'http://locahost:8000/api/elementos/{elemento.id}/')
        return elementos_preceptor


class ElementoComunicativoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElementoComunicativo
        fields = [
            'id',
            'preceptor',
            'ativo',
            'texto',
            'figura',
            'libras',
            'audioDescricao',
            'data',
            'tipo'
        ]
        depth = 1


class CardSerializer(serializers.ModelSerializer):

    titulo = serializers.SerializerMethodField()

    descricao = serializers.SerializerMethodField()

    opcoes = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            'id',
            'ativo',
            'data',
            'titulo',
            'descricao',
            'opcoes'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'ativo': {'read_only': True},
            'data': {'read_only': True}
        }

    def get_titulo(self, obj):
        elemento = ElementoComunicativo.objects.filter(id=obj.titulo_id).first()
        if(elemento != None):
            #fields
            return {
                'id': elemento.id, 
                'texto':elemento.texto,
                'figura':elemento.figura,
                'libras':elemento.libras,
                'audioDescricao':elemento.audioDescricao,
                'data':elemento.data,
                'tipo':elemento.tipo
            }

    def get_descricao(self, obj):
        elemento = ElementoComunicativo.objects.filter(id=obj.descricao_id).first()
        if(elemento != None):
            return {
                'id': elemento.id, 
                'texto':elemento.texto,
                'figura':elemento.figura,
                'libras':elemento.libras,
                'audioDescricao':elemento.audioDescricao,
                'data':elemento.data,
                'tipo':elemento.tipo
            }

    def get_opcoes(self, obj):
        final_opcoes = []
        opcoes = ElementoComunicativo.objects.filter(card_opcao__id=obj.id)
        if(opcoes != None):
            for opcao in opcoes:
                final_opcoes.append({
                'id': opcao.id, 
                'texto':opcao.texto,
                'figura':opcao.figura,
                'libras':opcao.libras,
                'audioDescricao':opcao.audioDescricao,
                'data':opcao.data,
                'tipo':opcao.tipo
            })
            return final_opcoes


class RoteiroSerializer(serializers.ModelSerializer):

    titulo = serializers.SerializerMethodField()
    descricao = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()

    class Meta:
        model = Roteiro
        fields = [
            'id',
            'ativo',
            'data',
            'titulo',
            'descricao',
            'cards'
        ]

    def get_titulo(self, obj):
        result = ElementoComunicativoService.find_elemento_by_id(obj.titulo_id)
        return {
                'id': result.id, 
                'texto':result.texto,
                'figura':result.figura,
                'libras':result.libras,
                'audioDescricao':result.audioDescricao,
                'data':result.data,
                'tipo':result.tipo
            }


    def get_descricao(self, obj):
        result = ElementoComunicativoService.find_elemento_by_id(obj.descricao_id)
        return {
                'id': result.id, 
                'texto':result.texto,
                'figura':result.figura,
                'libras':result.libras,
                'audioDescricao':result.audioDescricao,
                'data':result.data,
                'tipo':result.tipo
            }

    def get_cards(self, obj):
        cards = []
        result = CardService.find_cards_by_roteiro_id(obj.id)

        if(result != None):
            for card in result:
                
                opcoes = []
                if(card.opcoes.all() != None):
                    for opcao in card.opcoes.all():
                        opcoes.append({
                            'id': opcao.id, 
                            'texto':opcao.texto,
                            'figura':opcao.figura,
                            'libras':opcao.libras,
                            'audioDescricao':opcao.audioDescricao,
                            'data':opcao.data,
                            'tipo':opcao.tipo
                        })
                cards.append({
                    'id': card.id, 
                    'titulo':{
                            'id': card.titulo.id, 
                            'texto':card.titulo.texto,
                            'figura':card.titulo.figura,
                            'libras':card.titulo.libras,
                            'audioDescricao':card.titulo.audioDescricao,
                            'data':card.titulo.data,
                            'tipo':card.titulo.tipo
                        },
                    'descricao':{
                            'id': card.descricao.id, 
                            'texto':card.descricao.texto,
                            'figura':card.descricao.figura,
                            'libras':card.descricao.libras,
                            'audioDescricao':card.descricao.audioDescricao,
                            'data':card.descricao.data,
                            'tipo':card.descricao.tipo
                        },
                    'opcoes': opcoes,
                    'data':card.data
                })
        return cards


class PacienteSerializer(serializers.ModelSerializer):

    atendimentos = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        fields = [
            'id',
            'ativo',
            'nome',
            'atendimentos'
        ]

    def get_atendimentos(self, obj):
        elemento = ElementoComunicativo.objects.filter(id=obj.titulo_id).first()
        return f'http://127.0.0.1:8000/api/elementos/{elemento.id}/'


class AtendimentoSerializer(serializers.ModelSerializer):

    card = serializers.SerializerMethodField()
    opcao = serializers.SerializerMethodField()

    class Meta:
        model = Atendimento
        fields = [
            'id',
            'texto',
            'data',
            'paciente',
            'card',
            'opcao'
        ]

    def get_opcao(self, obj):
        result = ElementoComunicativoService.find_elemento_by_id(obj.opcao_id)
        return {
                'id': result.id, 
                'texto':result.texto,
                'figura':result.figura,
                'libras':result.libras,
                'audioDescricao':result.audioDescricao,
                'data':result.data,
                'tipo':result.tipo
            }

    def get_card(self, card):
        opcoes = []
        if(card.opcoes.all() != None):
            for opcao in card.opcoes.all():
                opcoes.append({
                    'id': opcao.id, 
                    'texto':opcao.texto,
                    'figura':opcao.figura,
                    'libras':opcao.libras,
                    'audioDescricao':opcao.audioDescricao,
                    'data':opcao.data,
                    'tipo':opcao.tipo
                })
                
        return {
            'id': card.id, 
            'titulo':{
                    'id': card.titulo.id, 
                    'texto':card.titulo.texto,
                    'figura':card.titulo.figura,
                    'libras':card.titulo.libras,
                    'audioDescricao':card.titulo.audioDescricao,
                    'data':card.titulo.data,
                    'tipo':card.titulo.tipo
                },
            'descricao':{
                    'id': card.descricao.id, 
                    'texto':card.descricao.texto,
                    'figura':card.descricao.figura,
                    'libras':card.descricao.libras,
                    'audioDescricao':card.descricao.audioDescricao,
                    'data':card.descricao.data,
                    'tipo':card.descricao.tipo
                },
            'opcoes': opcoes,
            'data':card.data
        }