from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import Atendimento, Card, ElementoComunicativo, Paciente, Preceptor, Roteiro
from .serializers import PreceptorSerializer, CardSerializer, RoteiroSerializer, AtendimentoSerializer, ElementoComunicativoSerializer, PacienteSerializer, AutenticacaoSerializer
from .permissions import UserLoginPermission
from .service import AtendimentoService, CardService, PreceptorService, ElementoComunicativoService, RoteiroService
from .utils import checkresult

@api_view(['POST'])
@permission_classes([UserLoginPermission])
def login(request, format=None):
    login = AutenticacaoSerializer(request.data)
    result = PreceptorService.check_user_credentials(login)
    if checkresult(result):
        return Response({"token": result['token'], "id": result['user_id']}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"erro": "erro de usuario ou senha"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class PreceptorViewSet(viewsets.ModelViewSet):
    queryset = Preceptor.objects.all()
    serializer_class = PreceptorSerializer

    @action(detail=True, methods=["post"], url_path='upload_avatar')
    def upload_avatar(self, request, pk=None):
        avatar = request.data.get('picture')
        PreceptorService.upload_avatar(pk, avatar)
        return Response(status=status.HTTP_200_OK)
    

class ElementoComunicativoViewSet(viewsets.ModelViewSet):
    queryset = ElementoComunicativo.objects.all()
    serializer_class = ElementoComunicativoSerializer

    @action(detail=True, methods=["post"], url_path='upload_figure')
    def upload_figure(self, request, pk=None):
        figure = request.data.get('picture')
        ElementoComunicativoService.upload_figure(pk, figure)
        return Response(status=status.HTTP_200_OK)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def create(self, request):
        titulo = ElementoComunicativoService.find_elemento_by_id(request.data['titulo'])
        descricao = ElementoComunicativoService.find_elemento_by_id(request.data['descricao'])
        opcoes = list(ElementoComunicativoService.find_elemento_by_id_list(request.data['opcoes']))
        result = CardService.create_card(titulo, descricao, opcoes)
        serializer = self.get_serializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoteiroViewSet(viewsets.ModelViewSet):
    queryset = Roteiro.objects.all()
    serializer_class = RoteiroSerializer

    def create(self, request):
        titulo = ElementoComunicativoService.find_elemento_by_id(request.data['titulo'])
        descricao = ElementoComunicativoService.find_elemento_by_id(request.data['descricao'])
        cards = list(CardService.find_cards_by_list(request.data['cards']))
        result = RoteiroService.create_roteiro(titulo, descricao, cards)
        serializer = self.get_serializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer

    def create(self, request):
        card = Card.objects.filter(id = request.data['card']).first()
        opcao = ElementoComunicativo.objects.filter(id= request.data['opcao']).first()
        result = AtendimentoService.create_atendimento(card, opcao)
        serializer = self.get_serializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
