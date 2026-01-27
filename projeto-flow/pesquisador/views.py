from pyexpat import model
from tempfile import template
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from proposals.models import Proposal
from submission.models import Submission

# Create your views here.
# def pesquisador_editais(request):
#   return render(request, 'pesquisador/editais.html')
def base(request):
  return render(request, './base/base.html')

class ProposalListView(ListView):
  model = Proposal
  template_name = 'pesquisador/editais.html'
  context_object_name = 'proposals'

# def pesquisador_projetos(request):
#   return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')

class SubmissionListView(ListView):
  model = Submission
  template_name = 'pesquisador/pesquisador_meus_projetos_tabela.html'
  context_object_name = 'submissions'

def pesquisador_projetos_detalhes(request):
  return render(request, 'pesquisador/pesquisador_meus_projetos_detalhes.html')

def pesquisador_adicionar_projeto(request):
  return render(request, 'pesquisador/adicionar_projeto.html')

def pesquisador_editar_projeto(request):
  return render(request, 'pesquisador/editar_projeto.html')