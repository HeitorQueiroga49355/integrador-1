from .views import ProposalListView, SubmissionListView, SubmissionCreateView, pesquisador_projetos_detalhes, base, SubmissionUpdateView
from . import views
from django.urls import path

urlpatterns = [
    path('base/', base, name='base'),

    path('', ProposalListView.as_view(), name='pesquisador-editais'),
    path('projetos/', SubmissionListView.as_view(), name='pesquisador-projetos'),
    path('projetos/adicionar/<int:proposal_id>/', SubmissionCreateView.as_view(), name='pesquisador-adicionar-projeto'),
    path('projetos/detalhes/<int:pk>/', pesquisador_projetos_detalhes, name='pesquisador-projetos-detalhes'), 
    path('projetos/detalhes/editar/<int:pk>/', SubmissionUpdateView.as_view(), name='pesquisador-projetos-detalhes-editar'), 
]