from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
    
    path('', views.proposals, name='proposals'),
    path('detalhes/<int:submission_id>/', views.details, name='details'),    #path('details/<int:proposal_id>/', views.details, name='details'),
    path('submissions/', views.submissions, name='submissions'),
    path('reviwers/', views.reviewers, name='reviewers'),
    path('editar/<int:proposal_id>/', views.proposal_edit, name='proposal_edit'),
    path('delete/<int:proposal_id>/', views.proposal_delete, name='proposal_delete'),
]