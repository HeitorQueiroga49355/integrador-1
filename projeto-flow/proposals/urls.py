from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
<<<<<<< Updated upstream
    path('', views.proposals, name='proposals'),
    path('detalhes/<int:submission_id>/', views.details, name='details'),
=======
    
    path('proposals/', views.proposals, name='proposals'),
    path('detalhes/<int:submission_id>/', views.details, name='details'),    #path('details/<int:proposal_id>/', views.details, name='details'),
>>>>>>> Stashed changes
    path('submissions/', views.submissions, name='submissions'),
    path('reviewers/', views.reviewers, name='reviewers'),
    path('editar/<int:proposal_id>/', views.proposal_edit, name='proposal_edit'),
    path('delete/<int:proposal_id>/', views.proposal_delete, name='proposal_delete'),
    
    # Novas URLs
    path('fechar/<int:proposal_id>/', views.close_proposal_manually, name='close_proposal'),
    path('exportar/excel/<int:proposal_id>/', views.export_proposal_results_excel, name='export_excel'),
    path('exportar/pdf/<int:proposal_id>/', views.export_proposal_results_pdf, name='export_pdf'),
]