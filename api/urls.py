from django.urls import path

from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from .views import login, PreceptorViewSet, ElementoComunicativoViewSet, RoteiroViewSet, CardViewSet, PacienteViewSet, AtendimentoViewSet

router = DefaultRouter()
router.register(r'preceptores', PreceptorViewSet, basename='preceptores')
router.register(r'elementos', ElementoComunicativoViewSet, basename='elementos')
router.register(r'roteiros', RoteiroViewSet, basename='roteiros')
router.register(r'cards', CardViewSet, basename='cards')
router.register(r'pacientes', PacienteViewSet, basename='pacientes')
router.register(r'atendimentos', AtendimentoViewSet, basename='atendimentos')


urlpatterns = [
    path('login/', login),
    ] + static('media/', document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
