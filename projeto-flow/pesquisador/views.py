from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.core.exceptions import PermissionDenied
from proposals.models import Proposal
from submission.models import Submission
from .forms import CreateSubmissionForm
from user.models import Profile
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Avg, Q

from .mixins import ResearcherRequiredMixin


# Create your views here.
# def pesquisador_editais(request):
#   return render(request, 'pesquisador/editais.html')
def base(request):
    return render(request, './base/base.html')


class ProposalListView(ResearcherRequiredMixin, ListView):
    model = Proposal
    template_name = 'pesquisador/editais.html'
    context_object_name = 'proposals'


# def pesquisador_projetos(request):
#   return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')

class SubmissionListView(ResearcherRequiredMixin, ListView):
    model = Submission
    template_name = 'pesquisador/pesquisador_meus_projetos_tabela.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == Profile.Role.RESEARCHER:
            # Otimiza a consulta para buscar o edital relacionado de uma só vez
            return Submission.objects.filter(researcher=user.profile).select_related('proposal')
        return Submission.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submissions = context['submissions']
        today = timezone.now().date()
        
        # Cache para classificações de editais para evitar consultas repetidas
        proposal_rankings = {}

        for sub in submissions:
            proposal = sub.proposal
            
            # Define o status padrão com base no banco de dados
            sub.display_status = sub.get_status_display()

            # Verifica se o edital está fechado para calcular a classificação
            if proposal.closing_date and proposal.closing_date < today:
                
                # Se ainda não classificamos este edital, fazemos agora
                if proposal.id not in proposal_rankings:
                    ranked_submission_ids = list(
                        Submission.objects.filter(proposal=proposal)
                        .annotate(avg_score=Avg('evaluations__score', filter=Q(evaluations__status='completed')))
                        .order_by('-avg_score')
                        .values_list('id', flat=True)
                    )
                    proposal_rankings[proposal.id] = ranked_submission_ids

                ranked_ids = proposal_rankings.get(proposal.id, [])
                if sub.id in ranked_ids:
                    # Verifica se a submissão está dentro do número de vagas
                    if ranked_ids.index(sub.id) < proposal.number_of_places:
                        sub.display_status = "Aprovado"
                    else:
                        sub.display_status = "Reprovado"
                else:
                    # Se não tem avaliação completa, é considerado reprovado após o fechamento
                    sub.display_status = "Reprovado"

        context['submissions'] = submissions
        return context


class SubmissionDetailView(ResearcherRequiredMixin, DetailView):
    model = Submission
    template_name = 'pesquisador/pesquisador_meus_projetos_detalhes.html'
    context_object_name = 'submission'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == Profile.Role.RESEARCHER:
            return Submission.objects.filter(researcher=user.profile)
        return Submission.objects.none()


class SubmissionCreateView(ResearcherRequiredMixin, CreateView):
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
        form.instance.proposal = get_object_or_404(Proposal, id=self.kwargs['proposal_id'])

        # Busca o perfil de pesquisador para associar ao projeto.
        user = self.request.user
        if not (user.is_authenticated and hasattr(user, 'profile') and user.profile.role == Profile.Role.RESEARCHER):
            # Lança um erro de permissão se o usuário não for um pesquisador.
            # A lógica de fallback para testes foi removida por ser insegura.
            raise PermissionDenied("Você não tem permissão para criar uma submissão.")

        form.instance.researcher = user.profile
        return super().form_valid(form)


class SubmissionUpdateView(ResearcherRequiredMixin, UpdateView):
    model = Submission
    form_class = CreateSubmissionForm
    template_name = 'pesquisador/editar_projeto.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.role == Profile.Role.RESEARCHER:
            return Submission.objects.filter(researcher=user.profile)
        return Submission.objects.none()

    def get_success_url(self):
        # Redireciona para a página de detalhes do projeto que acabou de ser editado
        return reverse('pesquisador-projetos-detalhes', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proposal'] = self.object.proposal
        return context
