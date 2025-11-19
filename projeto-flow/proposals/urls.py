from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.proposals, name='proposals'),
    path('details/', views.details, name='details'),
    #path('details/<int:proposal_id>/', views.details, name='details'),
    path('submissions/', views.submissions, name='submissions'),
    path('reviwers/', views.reviewers, name='reviewers'),
]