from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from pesquisador.models import Project
from pesquisador.forms import CreateProjectForm
from django.urls import reverse_lazy

# Create your views here.
# def pesquisador_editais(request):
#   return render(request, 'pesquisador/editais.html')

class PesquisadorEditaisView(TemplateView):
  template_name = 'pesquisador/editais.html'

def pesquisador_projetos(request):
    return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')
    
def base(request):
  return render(request, './base/base.html')

# def pesquisador_projetos(request):
#   return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')

class ProjectListView(ListView):
  model = Project
  template_name = 'pesquisador/pesquisador_meus_projetos_tabela.html'
  context_object_name = 'projects'

def pesquisador_projetos_detalhes(request):
  return render(request, 'pesquisador/pesquisador_meus_projetos_detalhes.html')

def pesquisador_adicionar_projeto(request):
  return render(request, 'pesquisador/adicionar_projeto.html')

def pesquisador_editar_projeto(request):
  return render(request, 'pesquisador/editar_projeto.html')

class ProjectCreateView(CreateView):
  model = Project
  form_class = CreateProjectForm
  template_name = 'pesquisador/adicionar_projeto.html'
  success_url = reverse_lazy('pesquisador-projetos')