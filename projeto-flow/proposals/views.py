from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import (
    ProposalForm,
    VersionProposalForm
    )


def proposals(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'proposals/proposals.html', {'form': ProposalForm(), 'success': True})
    else:
        form = ProposalForm()
    
    return render(request, 'proposals/proposals.html', {'form': form})

def details(request):
    if request.method == 'POST':
        form = VersionProposalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'proposals/details.html', {'form': VersionProposalForm(), 'success': True})
    else:
        form = VersionProposalForm()
    
    return render(request, 'proposals/details.html', {'form': form})

# if request.method == 'POST':
#         form = RectifyProposalForm(request.POST, request.FILES)
#         if form.is_valid():
#             rectify_proposal = form.save(commit=False)
#             # Se tiver uma proposal_id, associe
#             if proposal_id:
#                 rectify_proposal.proposal = Proposal.objects.get(id=proposal_id)
#             rectify_proposal.save()
#             return render(request, 'proposals/details.html', {'form': RectifyProposalForm(), 'success': True})
#     else:
#         form = RectifyProposalForm()
    
#     return render(request, 'proposals/details.html', {'form': form})

@login_required(login_url='login')
def submissions(request):
    context = {
        # dados do banco futuramente
    }
    return render(request, 'proposals/submissions.html', context)

@login_required(login_url='login')
def reviewers(request):
    context = {
        # dados do banco futuramente
    }
    return render(request, 'proposals/reviewers.html', context)