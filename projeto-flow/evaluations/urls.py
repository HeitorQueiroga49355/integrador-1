from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('evaluation/<int:submission_id>/', views.evaluation_create, name='evaluation_create'),
    path('avaliadores/', views.reviewers_list, name='reviewers_list'),
    path('avaliadores/deletar/<int:reviewer_id>/', views.reviewer_delete, name='reviewer_delete'),
    path('avaliadores/convidar/', views.send_invite, name='send_invite'),
    path('convite/<uuid:token>/', views.accept_invite, name='accept_invite'),
    path('avaliadores/adicionar-manual/', views.add_reviewer_manual, name='add_reviewer_manual'),
]