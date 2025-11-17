from django.urls import path
from . import views

urlpatterns = [
  path('base/', views.base, name='base'),

  path('pesquisador/meus-projetos/', views.pesquisador_projetos, name='pesquisador-projetos'),
  path('pesquisador/meus-projetos-detalhes/', views.pesquisador_projetos_detalhes, name='pesquisador-projetos-detalhes')
] 