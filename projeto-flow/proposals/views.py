from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProposalForm


def proposals(request):
    form = ProposalForm()
    return render(request, 'proposals/index.html', {'form': form})

def validate_proposal(request):
    form = ProposalForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse(form)
    return HttpResponse("Formulário inválido")