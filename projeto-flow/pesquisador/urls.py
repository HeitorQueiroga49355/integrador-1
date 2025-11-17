from django.urls import path
from . import views

urlpatterns = [
    path('pesquisador/tabela/', views.pesquisador_projetos, name='pesquisador-meus-projetos-tabela'),
    path('pesquisador/meus-projetos-detalhes/', views.pesquisador_proejetos_detalhes, name='pesquisador-meus-projetos-detalhes')
]
