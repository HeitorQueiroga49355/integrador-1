from .views import pesquisador_editais, pesquisador_projetos
from django.urls import path

urlpatterns = [
    path('', pesquisador_editais, name='pesquisador_editais'),
    path('projetos/', pesquisador_projetos, name='pesquisador_projetos'),
]