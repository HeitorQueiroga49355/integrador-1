from multiprocessing import context
from pyexpat import model
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from pesquisador.models import Project, Researcher
from pesquisador.forms import CreateProjectForm
from proposals.models import Proposal
from django.urls import reverse_lazy

# Create your views here.
# def pesquisador_editais(request):
#   return render(request, 'pesquisador/editais.html')

class PesquisadorEditaisView(ListView):
  model = Proposal
  template_name = 'pesquisador/editais.html'
  context_object_name = 'proposals'

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

# def pesquisador_adicionar_projeto(request):
#   return render(request, 'pesquisador/adicionar_projeto.html')

class ProjectCreateView(CreateView):
  model = Project
  form_class = CreateProjectForm
  template_name = 'pesquisador/adicionar_projeto.html'
  success_url = reverse_lazy('pesquisador-projetos')

def pesquisador_editar_projeto(request):
  return render(request, 'pesquisador/editar_projeto.html')

class ProjectCreateView(CreateView):
  model = Project
  form_class = CreateProjectForm
  template_name = 'pesquisador/adicionar_projeto.html'
  success_url = reverse_lazy('pesquisador-projetos')

  def form_valid(self, form):
    # Busca o perfil de pesquisador do usuário logado e associa ao projeto
    researcher = Researcher.objects.get(user=self.request.user)
    form.instance.researcher = researcher
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    # renomear o form no contexto
    context = super().get_context_data(**kwargs)
    context['form_projeto'] = context['form']
    return context
    