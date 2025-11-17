from .views import pesquisador_editais, pesquisador_projetos
from . import views
from django.urls import path

urlpatterns = [
    path('base/', views.base, name='base'),

    path('', pesquisador_editais, name='pesquisador_editais'),
    path('projetos/', pesquisador_projetos, name='pesquisador_projetos'),

    path('pesquisador/meus-projetos/', views.pesquisador_projetos, name='pesquisador-projetos'),
    path('pesquisador/meus-projetos-detalhes/', views.pesquisador_projetos_detalhes, name='pesquisador-projetos-detalhes')
]