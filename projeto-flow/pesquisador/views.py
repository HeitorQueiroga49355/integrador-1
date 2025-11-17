from django.shortcuts import render

# Create your views here.

def pesquisador_projetos(request):
  return render(request, 'pesquisador/pesquisador_meus_projetos_tabela.html')

def pesquisador_proejetos_detalhes(request):
  return render(request, 'pesquisador/pesquisador_meus_projetos_detalhes.html')