from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login(request):
    if request.user.is_authenticated:
        return redirect('pesquisador-editais')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # Tenta autenticar usando email ou username
        user = authenticate(request, username=email, password=password)

        # Se não funcionou com username, tenta encontrar por email
        if user is None:
            try:
                from .models import User
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            auth_login(request, user)

            # Define duração da sessão baseado no "lembre-me"
            if not remember_me:
                request.session.set_expiry(0)  # Expira quando o navegador fechar
            else:
                request.session.set_expiry(1209600)  # 2 semanas

            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')

            # Redireciona para a página que o usuário tentou acessar ou para editais
            next_url = request.GET.get('next', 'pesquisador-editais')
            return redirect(next_url)
        else:
            messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, './login/index.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('pesquisador-editais')

    return render(request, './register/index.html')

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.success(request, 'Você saiu da sua conta com sucesso.')
    return redirect('login')
