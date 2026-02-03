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

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import ReviewerInvite
from .forms import InviteForm, ExternalReviewerForm
from django.contrib import messages

from user.models import Profile

from django.contrib.auth import get_user_model
from django.db import transaction

from django.core.mail import get_connection
from django.contrib.auth.forms import PasswordResetForm

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



# Convidar um avaliador por email

def send_invite(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            try:
                invite = form.save()
                link = request.build_absolute_uri(
                    reverse('evaluations:accept_invite', args=[invite.token])
                )

                send_mail(
                    subject='Convite para Avaliador - Projeto Flow',
                    message=f'Olá!\nVocê foi convidado para fazer parte de nossa banca de Avaliadores. \nLink para cadastro: {link}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[invite.email],
                    fail_silently=False,
                )
                messages.success(request, f'Convite enviado com sucesso para {invite.email}!')

            except Exception as e:
                invite.delete() # Remove o convite se o email falhar
                messages.error(request, f'Erro ao enviar e-mail: {e}')
        else:
            messages.error(request, 'Este e-mail já foi convidado ou é inválido.')

    return redirect('evaluations:reviewers_list')

def accept_invite(request, token):
    invite = get_object_or_404(ReviewerInvite, token=token)

    if invite.accepted:
        return render(request, 'evaluations/invite_error.html', {'message': 'Este convite já foi utilizado.'})

    if request.method == 'POST':
        form = ExternalReviewerForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    User = get_user_model()
                    email = invite.email

                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Erro: Já existe um usuário com este e-mail.')
                        return render(request, 'evaluations/invite_register.html', {'form': form, 'email': email})

                    # Cria o Usuário de Login
                    new_user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=form.cleaned_data['password']
                    )
                    # Pega o primeiro nome para o User
                    new_user.first_name = form.cleaned_data['name'].split()[0]
                    new_user.save()

                    # Cria/Atualiza o Profile (Role = Avaliador)
                    profile, created = Profile.objects.get_or_create(user=new_user)
                    profile.role = Profile.Role.EVALUATOR
                    profile.save()

                    # Cria o Reviewer
                    reviewer = form.save(commit=False)
                    reviewer.user = new_user
                    reviewer.email = email  # Salva email no reviewer também (estrutura antiga)
                    reviewer.institution = Institution.objects.first()
                    reviewer.save()

                    # Invalida o convite
                    invite.accepted = True
                    invite.save()

                return render(request, 'evaluations/invite_success.html')

            except Exception as e:
                print(f"ERRO NO SERVIDOR: {e}")
                messages.error(request, f'Erro interno ao criar conta: {e}')

        else:
            print("--- ERRO DE VALIDAÇÃO DO FORMULÁRIO ---")
            print(form.errors)
            messages.error(request, 'Verifique os dados preenchidos (senhas ou CPF inválido).')

    else:
        form = ExternalReviewerForm()

    return render(request, 'evaluations/invite_register.html', {'form': form, 'email': invite.email})


# --- Função de adicionar manualmente ---
def add_reviewer_manual(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', '').strip()
        cpf = request.POST.get('cpf')
        expertise = request.POST.get('expertise')
        password = request.POST.get('password', '').strip()

        User = get_user_model()
        user = None
        created_new_user = False

        try:
            with transaction.atomic():
                # Verifica se o usuário JÁ existe
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)

                    # Se ele já for avaliador, aí sim paramos
                    if Reviewer.objects.filter(user=user).exists():
                        messages.warning(request, 'Este usuário já está cadastrado como Avaliador.')
                        return redirect('evaluations:reviewers_list')

                    # Se existe mas não é avaliador, vamos promovê-lo
                    print(f"--- USUÁRIO EXISTENTE ENCONTRADO: {email}. PROMOVENDO... ---")

                else:
                    # Se não existe, cria um novo
                    if not password:
                        messages.error(request, 'Senha é obrigatória para novos usuários.')
                        return redirect('evaluations:reviewers_list')

                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.first_name = name.split()[0]
                    user.save()
                    created_new_user = True
                    print(f"--- NOVO USUÁRIO CRIADO: {email} ---")

                # Garante que o Profile é de avaliador (ou atualiza se já existir)
                profile, _ = Profile.objects.get_or_create(user=user)
                profile.role = 'avaliador' # Profile.Role.EVALUATOR
                profile.save()

                # Cria o vínculo de Reviewer
                Reviewer.objects.create(
                    user=user,
                    name=name, email=email, cpf=cpf, expertise=expertise,
                    institution=Institution.objects.first()
                )

            # --- ENVIO DE E-MAIL  ---
            subject = 'Projeto Flow - Novo Perfil de Acesso'

            if created_new_user:
                # E-mail com SENHA
                message = (
                    f"Olá, {name}.\n\n"
                    f"Seu cadastro de Avaliador foi criado.\n\n"
                    f"Login: {email}\n"
                    f"Senha: {password}\n\n"
                    f"Acesse o sistema para validar."
                )
            else:
                # E-mail SEM SENHA
                message = (
                    f"Olá, {name}.\n\n"
                    f"Seu perfil foi atualizado. Agora você também possui permissões de Avaliador.\n\n"
                    f"Acesse o sistema com seu login e senha atuais."
                )

            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

            if created_new_user:
                messages.success(request, 'Avaliador criado e senha enviada!')
            else:
                messages.success(request, 'Usuário existente promovido a Avaliador com sucesso!')

        except Exception as e:
            print(f"ERRO: {e}")
            messages.error(request, f'Erro ao processar: {e}')

    return redirect('evaluations:reviewers_list')

# --- Função de promover avaliador a gestor ---
def promote_to_manager(request, reviewer_id):
    # Busca o avaliador
    reviewer = get_object_or_404(Reviewer, id=reviewer_id)

    try:
        user = reviewer.user # Guardamos a referência do usuário antes de deletar o reviewer

        if not user:
            messages.error(request, 'Este avaliador não possui um usuário associado.')
            return redirect('evaluations:reviewers_list')

        with transaction.atomic():
            # Atualiza o perfil para Manager
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = Profile.Role.MANAGER
            profile.save()

            # Deleta o registro de Avaliador
            # Isso fará com que ele suma da lista automaticamente
            reviewer.delete()

        messages.success(request, f'Sucesso! {user.first_name} foi promovido a Manager e removido da lista de avaliadores.')

    except Exception as e:
        messages.error(request, f'Erro ao promover usuário: {e}')

    return redirect('evaluations:reviewers_list')