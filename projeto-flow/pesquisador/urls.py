from .views import ProposalListView, SubmissionListView, pesquisador_projetos_detalhes, base, pesquisador_adicionar_projeto, pesquisador_editar_projeto
from . import views
from django.urls import path

urlpatterns = [
    path('base/', base, name='base'),

    path('', ProposalListView.as_view(), name='pesquisador-editais'),
    path('projetos/', SubmissionListView.as_view(), name='pesquisador-projetos'),
    path('projetos/adicionar/', pesquisador_adicionar_projeto, name='pesquisador-adicionar-projeto'),
    path('projetos/detalhes/', pesquisador_projetos_detalhes, name='pesquisador-projetos-detalhes'), 
    path('projetos/detalhes/editar/', pesquisador_editar_projeto, name='pesquisador-projetos-detalhes-editar'), 
]