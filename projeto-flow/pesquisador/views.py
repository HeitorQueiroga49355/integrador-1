from pyexpat import model
from tempfile import template
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView
from proposals.models import Proposal
from submission.models import Submission
from .forms import CreateSubmissionForm
from .models import Researcher
from django.urls import reverse_lazy

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

  def get_queryset(self):
    # if hasattr(self.request.user, 'researcher_profile'):
    #     return Submission.objects.filter(researcher=self.request.user.researcher_profile)
    # return Submission.objects.none()
    # Temporariamente, para fins de teste, exibe todas as submissões.
    return Submission.objects.all()

def pesquisador_projetos_detalhes(request, pk):
  submission = get_object_or_404(Submission, pk=pk)
  return render(request, 'pesquisador/pesquisador_meus_projetos_detalhes.html', {'submission': submission})

class SubmissionCreateView(CreateView):
  model = Submission
  form_class = CreateSubmissionForm
  template_name = 'pesquisador/adicionar_projeto.html'
  success_url = reverse_lazy('pesquisador-projetos')
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['proposal'] = get_object_or_404(Proposal, pk=self.kwargs['proposal_id'])
      return context

  def form_valid(self, form):
    # Associa o edital (Proposal) ao projeto, buscando pelo ID na URL.
    proposal = get_object_or_404(Proposal, id=self.kwargs['proposal_id'])
    form.instance.proposal = proposal

    # Busca o perfil de pesquisador para associar ao projeto.
    try:
        # Tenta buscar o perfil de pesquisador do usuário logado.
        researcher = self.request.user.researcher_profile
    except (AttributeError, Researcher.user.RelatedObjectDoesNotExist):
        # SOLUÇÃO TEMPORÁRIA PARA TESTES:
        # Se o usuário não tiver um perfil de pesquisador (ex: admin ou não logado),
        # o código pega o primeiro pesquisador do banco de dados como autor.
        # Certifique-se de que existe pelo menos um pesquisador cadastrado no seu sistema.
        researcher = Researcher.objects.first()
        if not researcher:
            raise Exception("Nenhum pesquisador encontrado no banco de dados. Crie um no painel de admin para poder testar.")
    form.instance.researcher = researcher
    return super().form_valid(form)

def pesquisador_editar_projeto(request):
  return render(request, 'pesquisador/editar_projeto.html')