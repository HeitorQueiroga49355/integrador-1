from .views import pesquisador_editais, pesquisador_projetos, pesquisador_projetos_detalhes, base
# from . import views
from django.urls import path

urlpatterns = [
    path('base/', base, name='base'),

    path('', pesquisador_editais, name='pesquisador-editais'),
    path('projetos/', pesquisador_projetos, name='pesquisador-projetos'),
    path('projetos/detalhes/', pesquisador_projetos_detalhes, name='pesquisador-projetos-detalhes')
]