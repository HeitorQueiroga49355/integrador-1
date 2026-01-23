from .views import PesquisadorEditaisView, ProjectListView, ProjectCreateView, pesquisador_projetos_detalhes, base, pesquisador_editar_projeto
from django.urls import path

urlpatterns = [
    path('base/', base, name='base'),

    # path('', pesquisador_editais, name='pesquisador-editais'),
    path('', PesquisadorEditaisView.as_view(), name='pesquisador-editais'),
    # path('projetos/', pesquisador_projetos, name='pesquisador-projetos'),
    path('projetos/', ProjectListView.as_view(), name='pesquisador-projetos'),
    path('projetos/adicionar/', ProjectCreateView.as_view(), name='pesquisador-adicionar-projeto'),
    path('projetos/detalhes/', pesquisador_projetos_detalhes, name='pesquisador-projetos-detalhes'), 
    path('projetos/detalhes/editar/', pesquisador_editar_projeto, name='pesquisador-projetos-detalhes-editar'), 
]