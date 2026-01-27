from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def pesquisador_editais(request):
  return render(request, 'pesquisador/editais.html')

@login_required(login_url='login')
def pesquisador_projetos(request):
    return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')
    
@login_required(login_url='login')
def base(request):
  return render(request, './base/base.html')

@login_required(login_url='login')
def pesquisador_projetos_detalhes(request):
  return render(request, 'pesquisador/pesquisador_meus_projetos_detalhes.html')

@login_required(login_url='login')
def pesquisador_adicionar_projeto(request):
  return render(request, 'pesquisador/adicionar_projeto.html')

@login_required(login_url='login')
def pesquisador_editar_projeto(request):
  return render(request, 'pesquisador/editar_projeto.html')