from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import Profile
from .utils import get_default_page_alias_by_user
from django.contrib.messages import get_messages


from django.contrib.auth.decorators import login_required


def index_view(request):
    return redirect(get_default_page_alias_by_user(request.user))


class LoginView(AuthLoginView):
    template_name = './login/index.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Set session to expire when browser closes
            self.request.session.set_expiry(0)
        else:
            # Keep session for 2 weeks
            self.request.session.set_expiry(1209600)

        messages.success(self.request, 'Login realizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'E-mail ou senha incorretos.')
        return super().form_invalid(form)


class RegisterView(FormView):
    template_name = './register/index.html'
    form_class = RegisterForm
    success_url = reverse_lazy('pesquisador-editais')

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users
        if request.user.is_authenticated:
            return redirect('pesquisador-editais')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        # Explicitly specify the backend for login
        login(self.request, user, backend='user.backends.EmailBackend')
        messages.success(self.request, 'Cadastro realizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao realizar cadastro. Verifique os campos.')
        return super().form_invalid(form)


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        # Limpa mensagens pendentes
        storage = get_messages(request)
        for _ in storage:
            pass

        messages.info(request, 'Você saiu da sua conta.')
        return super().dispatch(request, *args, **kwargs)




@login_required
def dashboard_router(request):
    user = request.user
    
    # Verifica se o usuário tem perfil
    if not hasattr(user, 'profile'):
        return redirect('proposals:proposals')

    role = user.profile.role

    if role == 'manager':
        # Manager -> Lista de Avaliadores
        return redirect('proposals:proposals')
        
    elif role == 'evaluator':
        # Avaliador -> Minhas Avaliações 
        return redirect('evaluations:my_evaluations')
        
    else:
        # Pesquisador (padrão) -> Editais
        return redirect('proposals:proposals')