from django.contrib import admin

from .models import Atendimento, Card, Paciente, Preceptor, Roteiro, ElementoComunicativo

admin.site.register(Atendimento)
admin.site.register(Card)
admin.site.register(Paciente)
admin.site.register(Preceptor)
admin.site.register(Roteiro)
admin.site.register(ElementoComunicativo)