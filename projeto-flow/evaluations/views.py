from django.shortcuts import render, redirect, get_object_or_404

from .models import Evaluation, Reviewer
from .forms import EvaluationForm, ReviewerForm


from submission.models import Submission
from institution.models import Institution

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import ReviewerInvite
from .forms import InviteForm, ExternalReviewerForm
from django.contrib import messages


def evaluation_create(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    evaluation = Evaluation.objects.filter(submission=submission).first()

    
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.submission = submission
            
            # Pega a instituição logada (ajustar depois quando tiver login real)
            ev.institution = Institution.objects.first() 
            
            ev.score = (
                ev.note_scientific_relevance + 
                ev.note_feasibility_methodological + 
                ev.note_expected_results
            )
            ev.save()
            return redirect('proposals:submissions')
    else:
        form = EvaluationForm(instance=evaluation)

    return render(request, 'evaluations/evaluation_form.html', {
        'form': form,
        'submission': submission, # Passamos a submissão para o template
        'existing_evaluation': evaluation
    })


def reviewers_list(request):
    # SALVAR NOVO AVALIADOR
    if request.method == 'POST':
        form = ReviewerForm(request.POST)
        if form.is_valid():
            reviewer = form.save(commit=False)
            reviewer.institution = Institution.objects.first()
            reviewer.save()
            return redirect('evaluations:reviewers_list')
    else:
        form = ReviewerForm()

    # LISTAR AVALIADORES
    reviewers = Reviewer.objects.all().order_by('-created_at')
    
    context = {
        'reviewers': reviewers,
        'form': form
    }
    return render(request, 'proposals/reviewers.html', context)

def reviewer_delete(request, reviewer_id):
    reviewer = get_object_or_404(Reviewer, id=reviewer_id)
    if request.method == 'POST':
        reviewer.delete()

    return redirect('evaluations:reviewers_list')



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
    # Busco o convite pelo token
    invite = get_object_or_404(ReviewerInvite, token=token)
    
    if invite.accepted:
        return render(request, 'evaluations/invite_error.html', {'message': 'Este convite já foi utilizado.'})

    if request.method == 'POST':
        form = ExternalReviewerForm(request.POST)
        if form.is_valid():
            # Cria o avaliador
            reviewer = form.save(commit=False)
            reviewer.email = invite.email # Usa o email do convite
            reviewer.institution = Institution.objects.first() # Vincula na instituição padrão
            reviewer.save()
            
            # Marca o convite como usado
            invite.accepted = True
            invite.save()
            
            return render(request, 'evaluations/invite_success.html')
    else:
        form = ExternalReviewerForm()

    return render(request, 'evaluations/invite_register.html', {'form': form, 'email': invite.email})