import cloudinary

from rest_framework.authtoken.models import Token

from .models import Atendimento, Card, ElementoComunicativo, Paciente, Preceptor, Roteiro

from .utils import checkresult


class TokenService():
    
    def get_user_token(user_pk):
        result = Token.objects.filter(user_id=user_pk)
        return result.get() if checkresult(result) else None


class PreceptorService():
    
    def check_user_credentials(login):
        result = Preceptor.objects.filter(username=login.data['usuario']).filter(password=login.data['senha'])
        if checkresult(result):
            token = TokenService.get_user_token(result.get().id)
            return {"token": token.key, "user_id": result.get().id}
        else: return None

    def find_preceptor_by_id(user_id):
        result = Preceptor.objects.filter(pk=user_id)
        return checkresult(result) 

    def upload_avatar(user_id, avatar):
        upload_data = cloudinary.uploader.upload(avatar)
        user = PreceptorService.find_preceptor_by_id(user_id)
        user.avatar = upload_data['url']
        user.save()


class ElementoComunicativoService():

    def find_elemento_by_id_list(id_list):
        result = list(ElementoComunicativo.objects.filter(pk__in=id_list))
        return result if checkresult(result) else []

    def find_elemento_by_id(element_id):
        result = ElementoComunicativo.objects.filter(pk=element_id)
        return result.get() if checkresult(result) else None

    def find_elemento_by_type(type):
        result = list(ElementoComunicativo.objects.filter(tipo=type))
        return checkresult(result)

    def upload_figure(element_id, figure):
        upload_data = cloudinary.uploader.upload(figure)
        element = ElementoComunicativoService.find_elemento_by_id(element_id)
        element.figura = upload_data['url']
        element.save()


class CardService():

    def create_card(titulo, descricao, lista_opcoes):
        card = Card.objects.create()
        card.titulo = titulo
        card.descricao = descricao
        card.opcoes.set(lista_opcoes)
        card.save()
        return card

    def find_card_by_id(card_id):
        result = Card.objects.filter(pk=card_id)
        return checkresult(result)

    def find_cards_by_list(id_list):
        result = Card.objects.filter(pk__in=id_list)
        return result if checkresult(result) else []

    def find_cards_by_roteiro_id(roteiro_id):
        result = list(Card.objects.filter(roteiro_cards__id=roteiro_id))
        return result if checkresult(result) else []


class RoteiroService():

    def create_roteiro(titulo, descricao, lista_cards):
        roteiro = Roteiro.objects.create()
        roteiro.titulo = titulo
        roteiro.descricao = descricao
        roteiro.cards.set(lista_cards)
        roteiro.save()
        return roteiro

    def find_roteiro_by_id(roteiro_id):
        result = Roteiro.objects.filter(pk=roteiro_id)
        return result

class AtendimentoService():

    def create_atendimento(card, opcao):
        atendimento = Roteiro.objects.create()
        atendimento.texto = "titulo"
        atendimento.paciente = Paciente.objects.first()
        atendimento.cards.set([card])
        atendimento.opcao.set([opcao])
        atendimento.save()
        return atendimento