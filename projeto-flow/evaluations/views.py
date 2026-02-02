from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q, Avg
from .models import Evaluation, Reviewer, SubmissionAssignment
from .forms import EvaluationForm, ReviewerForm
from submission.models import Submission
from proposals.models import Proposal
from institution.models import Institution
from .services import SubmissionDistributionService, auto_distribute_on_proposal_close


# ============= VIEWS DE AVALIAÇÃO =============

def evaluation_create(request, submission_id):
    """
    View para criar/editar avaliação de uma submissão.
    O avaliador só pode avaliar submissões atribuídas a ele.
    """
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Busca o avaliador baseado no usuário logado
    # TODO: Ajustar quando tiver autenticação real
    try:
        reviewer = Reviewer.objects.filter(
            institution=Institution.objects.first()
        ).first()
    except Reviewer.DoesNotExist:
        messages.error(request, "Você não está cadastrado como avaliador.")
        return redirect('proposals:submissions')
    
    # Verifica se este avaliador tem atribuição para esta submissão
    try:
        assignment = SubmissionAssignment.objects.get(
            submission=submission,
            reviewer=reviewer
        )
    except SubmissionAssignment.DoesNotExist:
        messages.error(request, "Você não está autorizado a avaliar esta submissão.")
        return redirect('proposals:submissions')
    
    # Busca ou cria a avaliação
    evaluation = Evaluation.objects.filter(
        assignment=assignment,
        submission=submission,
        reviewer=reviewer
    ).first()
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.assignment = assignment
            ev.submission = submission
            ev.reviewer = reviewer
            ev.institution = submission.proposal.institution
            ev.proposal = submission.proposal
            
            # Se está salvando com dados completos, muda status
            if ev.project_report and ev.note_scientific_relevance:
                ev.status = 'completed'
            else:
                ev.status = 'in_progress'
            
            ev.save()
            
            messages.success(request, "Avaliação salva com sucesso!")
            return redirect('evaluations:my_evaluations')
    else:
        form = EvaluationForm(instance=evaluation)
    
    return render(request, 'evaluations/evaluation_form.html', {
        'form': form,
        'submission': submission,
        'assignment': assignment,
        'existing_evaluation': evaluation
    })


def my_evaluations(request):
    """
    Lista todas as avaliações atribuídas ao avaliador logado.
    """
    # TODO: Ajustar quando tiver autenticação real
    try:
        reviewer = Reviewer.objects.filter(
            institution=Institution.objects.first()
        ).first()
    except Reviewer.DoesNotExist:
        messages.error(request, "Você não está cadastrado como avaliador.")
        return redirect('proposals:proposals')
    
    # Busca todas as atribuições do avaliador
    assignments = SubmissionAssignment.objects.filter(
        reviewer=reviewer
    ).select_related('submission', 'submission__proposal').order_by('-assigned_date')
    
    # Separa por status
    pending = []
    in_progress = []
    completed = []
    
    for assignment in assignments:
        try:
            evaluation = Evaluation.objects.get(assignment=assignment)
            status = evaluation.status
        except Evaluation.DoesNotExist:
            status = 'pending'
        
        data = {
            'assignment': assignment,
            'submission': assignment.submission,
            'proposal': assignment.submission.proposal,
            'status': status
        }
        
        if status == 'pending':
            pending.append(data)
        elif status == 'in_progress':
            in_progress.append(data)
        else:
            completed.append(data)
    
    context = {
        'reviewer': reviewer,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed,
        'total': len(pending) + len(in_progress) + len(completed)
    }
    
    return render(request, 'evaluations/my_evaluations.html', context)


# ============= VIEWS DE GERENCIAMENTO DE AVALIADORES =============

def reviewers_list(request):
    """
    Lista e gerencia avaliadores.
    """
    if request.method == 'POST':
        form = ReviewerForm(request.POST)
        if form.is_valid():
            reviewer = form.save(commit=False)
            reviewer.institution = Institution.objects.first()
            reviewer.save()
            messages.success(request, f"Avaliador {reviewer.name} cadastrado com sucesso!")
            return redirect('evaluations:reviewers_list')
    else:
        form = ReviewerForm()
    
    reviewers = Reviewer.objects.all().order_by('-created_at')
    
    # Estatísticas de cada avaliador
    reviewers_data = []
    for reviewer in reviewers:
        total_assignments = SubmissionAssignment.objects.filter(reviewer=reviewer).count()
        pending = Evaluation.objects.filter(
            reviewer=reviewer,
            status='pending'
        ).count()
        completed = Evaluation.objects.filter(
            reviewer=reviewer,
            status='completed'
        ).count()
        
        reviewers_data.append({
            'reviewer': reviewer,
            'total_assignments': total_assignments,
            'pending': pending,
            'completed': completed
        })
    
    context = {
        'reviewers_data': reviewers_data,
        'form': form
    }
    
    return render(request, 'evaluations/reviewers_list.html', context)


def reviewer_delete(request, reviewer_id):
    """
    Remove um avaliador.
    """
    reviewer = get_object_or_404(Reviewer, id=reviewer_id)
    
    if request.method == 'POST':
        # Verifica se o avaliador tem avaliações pendentes
        pending_evaluations = Evaluation.objects.filter(
            reviewer=reviewer,
            status__in=['pending', 'in_progress']
        ).count()
        
        if pending_evaluations > 0:
            messages.error(
                request,
                f"Não é possível remover {reviewer.name}. Existem {pending_evaluations} avaliações pendentes."
            )
        else:
            name = reviewer.name
            reviewer.delete()
            messages.success(request, f"Avaliador {name} removido com sucesso!")
    
    return redirect('evaluations:reviewers_list')


# ============= VIEWS DE DISTRIBUIÇÃO =============

def distribute_submissions(request, proposal_id):
    """
    Distribui as submissões de um edital para os avaliadores.
    """
    proposal = get_object_or_404(Proposal, id=proposal_id)
    
    if request.method == 'POST':
        # Pega parâmetros do formulário
        reviewers_per_submission = int(request.POST.get('reviewers_per_submission', 2))
        submissions_per_reviewer = int(request.POST.get('submissions_per_reviewer', 3))
        
        # TODO: Pegar usuário logado quando tiver autenticação
        assigned_by = None
        
        try:
            service = SubmissionDistributionService(proposal)
            stats = service.distribute_submissions(
                submissions_per_reviewer=submissions_per_reviewer,
                reviewers_per_submission=reviewers_per_submission,
                assigned_by=assigned_by
            )
            
            messages.success(
                request,
                f"Distribuição realizada! {stats['assignments_created']} atribuições criadas, "
                f"{stats['notifications_sent']} notificações enviadas."
            )
            
            if stats['errors']:
                for error in stats['errors']:
                    messages.warning(request, error)
                    
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Erro ao distribuir: {str(e)}")
        
        return redirect('evaluations:distribution_status', proposal_id=proposal_id)
    
    # GET: Mostra formulário de distribuição
    # Busca estatísticas atuais
    service = SubmissionDistributionService(proposal)
    stats = service.get_distribution_stats()
    
    context = {
        'proposal': proposal,
        'stats': stats
    }
    
    return render(request, 'evaluations/distribute_form.html', context)


def distribution_status(request, proposal_id):
    """
    Mostra o status da distribuição de um edital.
    """
    proposal = get_object_or_404(Proposal, id=proposal_id)
    service = SubmissionDistributionService(proposal)
    stats = service.get_distribution_stats()
    
    # Busca todas as submissões e suas atribuições
    submissions = Submission.objects.filter(proposal=proposal).prefetch_related(
        'assignments__reviewer'
    )
    
    submissions_data = []
    for submission in submissions:
        assignments = SubmissionAssignment.objects.filter(
            submission=submission
        ).select_related('reviewer')
        
        reviewers_info = []
        for assignment in assignments:
            try:
                evaluation = Evaluation.objects.get(assignment=assignment)
                status = evaluation.status
                score = evaluation.score
            except Evaluation.DoesNotExist:
                status = 'pending'
                score = None
            
            reviewers_info.append({
                'reviewer': assignment.reviewer,
                'status': status,
                'score': score,
                'assigned_date': assignment.assigned_date
            })
        
        submissions_data.append({
            'submission': submission,
            'reviewers': reviewers_info,
            'reviewer_count': len(reviewers_info)
        })
    
    context = {
        'proposal': proposal,
        'stats': stats,
        'submissions_data': submissions_data
    }
    
    return render(request, 'evaluations/distribution_status.html', context)


def auto_distribute(request, proposal_id):
    """
    Distribui automaticamente quando o edital é fechado.
    """
    if request.method == 'POST':
        result = auto_distribute_on_proposal_close(proposal_id)
        
        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
    
    return redirect('evaluations:distribution_status', proposal_id=proposal_id)


# ============= VIEWS DE RELATÓRIOS =============

def evaluation_report(request, proposal_id):
    """
    Gera relatório de avaliações de um edital.
    """
    proposal = get_object_or_404(Proposal, id=proposal_id)
    
    # Busca todas as submissões com suas avaliações
    submissions = Submission.objects.filter(proposal=proposal)
    
    report_data = []
    for submission in submissions:
        evaluations = Evaluation.objects.filter(
            submission=submission,
            status='completed'
        )
        
        if evaluations.exists():
            avg_score = evaluations.aggregate(Avg('score'))['score__avg']
            
            report_data.append({
                'submission': submission,
                'evaluations': evaluations,
                'avg_score': avg_score,
                'evaluation_count': evaluations.count()
            })
    
    # Ordena por média de pontuação
    report_data.sort(key=lambda x: x['avg_score'] or 0, reverse=True)
    
    context = {
        'proposal': proposal,
        'report_data': report_data
    }
    
    return render(request, 'evaluations/evaluation_report.html', context)