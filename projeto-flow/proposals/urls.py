from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.proposals, name='proposals'),
    # path('proposals/new/', views.new_proposal, name='new_proposal'),
    path('validate/', views.validate_proposal, name='validate_proposal'),
    # path('proposals/<int:proposal_id>/', views.proposal_detail, name='proposal_detail'),
]