from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    # Avaliações
    path('avaliar/<int:submission_id>/', views.evaluation_create, name='evaluation_create'),
    path('minhas-avaliacoes/', views.my_evaluations, name='my_evaluations'),
    
    # Avaliadores
    path('avaliadores/', views.reviewers_list, name='reviewers_list'),
    path('avaliadores/deletar/<int:reviewer_id>/', views.reviewer_delete, name='reviewer_delete'),
    
    # Distribuição
    path('distribuir/<int:proposal_id>/', views.distribute_submissions, name='distribute_submissions'),
    path('distribuicao/status/<int:proposal_id>/', views.distribution_status, name='distribution_status'),
    path('distribuicao/auto/<int:proposal_id>/', views.auto_distribute, name='auto_distribute'),
    
    # Relatórios
    path('relatorio/<int:proposal_id>/', views.evaluation_report, name='evaluation_report'),
]