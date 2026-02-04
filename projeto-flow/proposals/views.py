from django.shortcuts import render, get_object_or_404, redirect

from user.models import Profile
from user.utils import get_default_page_alias_by_user
from .forms import (
    ProposalForm,
)
from submission.models import Submission
from django.db.models import Q
from institution.models import Institution
from .models import Proposal
from datetime import datetime


def proposals(request):
    if not request.user.is_authenticated or request.user.profile.role not in [Profile.Role.MANAGER]:
        return redirect(get_default_page_alias_by_user(request.user))
    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES)
        if form.is_valid():
            new_proposal = form.save(commit=False)
            institution = Institution.objects.first()

            if institution:
                new_proposal.institution = institution
                new_proposal.save()
                return redirect('proposals:proposals')
            else:
                form.add_error(None, "Nenhuma instituição encontrada para vincular o edital.")
    else:
        form = ProposalForm()

    today = datetime.now().date()

    editais_abertos = Proposal.objects.filter(closing_date__gte=today).order_by('-opening_date')
    editais_fechados = Proposal.objects.filter(closing_date__lt=today).order_by('-opening_date')

    return render(request, 'proposals/proposals.html', {
        'editais_abertos': editais_abertos,
        'editais_fechados': editais_fechados,
        'form': form
    })


def details(request, submission_id):
    if not request.user.is_authenticated or request.user.profile.role not in [Profile.Role.MANAGER]:
        return redirect(get_default_page_alias_by_user(request.user))
    submission = get_object_or_404(Submission, id=submission_id)

    context = {
        'submission': submission
    }
    return render(request, 'proposals/details.html', context)


def submissions(request):
    if not request.user.is_authenticated or request.user.profile.role not in [Profile.Role.MANAGER]:
        return redirect(get_default_page_alias_by_user(request.user))
    search_query = request.GET.get('q')

    if search_query:
        submissions_list = Submission.objects.filter(
            Q(title__icontains=search_query) |
            Q(researcher__user__first_name__icontains=search_query) |
            Q(researcher__user__username__icontains=search_query)
        )
    else:
        submissions_list = Submission.objects.all().order_by('-created_at')
    context = {
        'submissions': submissions_list
    }
    return render(request, 'proposals/submissions.html', context)


def reviewers(request):
    if not request.user.is_authenticated or request.user.profile.role not in [Profile.Role.MANAGER]:
        return redirect(get_default_page_alias_by_user(request.user))
    context = {
        # dados do banco futuramente
    }
    return render(request, 'proposals/reviewers.html', context)


def proposal_edit(request, proposal_id):
    if not request.user.is_authenticated or request.user.profile.role not in [Profile.Role.MANAGER]:
        return redirect(get_default_page_alias_by_user(request.user))
    proposal = get_object_or_404(Proposal, id=proposal_id)

    if request.method == 'POST':
        form = ProposalForm(request.POST, request.FILES, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect('proposals:proposals')
    else:
        return redirect('proposals:proposals')


def proposal_delete(request, proposal_id):
    if not request.user.is_authenticated or request.user.profile.role not in [Profile.Role.MANAGER]:
        return redirect(get_default_page_alias_by_user(request.user))
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if request.method == 'POST':
        proposal.delete()

    return redirect('proposals:proposals')
