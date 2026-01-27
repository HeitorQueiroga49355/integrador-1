from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('evaluation/<int:submission_id>/', views.evaluation_create, name='evaluation_create'),
    path('avaliadores/', views.reviewers_list, name='reviewers_list'),
    path('avaliadores/deletar/<int:reviewer_id>/', views.reviewer_delete, name='reviewer_delete'),
]