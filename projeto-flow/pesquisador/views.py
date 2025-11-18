from django.shortcuts import render

# Create your views here.
def pesquisador_editais(request):
  return render(request, 'pesquisador/editais.html')

def pesquisador_projetos(request):
    return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')
    
def base(request):
  return render(request, './base/base.html')

def pesquisador_projetos(request):
  return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')

def pesquisador_projetos_detalhes(request):
  return render(request, 'pesquisador/pesquisador_meus_projetos_detalhes.html')