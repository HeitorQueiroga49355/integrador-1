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

from user.models import Profile

from django.contrib.auth import get_user_model
from django.db import transaction

from django.core.mail import get_connection
from django.contrib.auth.forms import PasswordResetForm


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
        'submission': submission, 
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