from django.shortcuts import render, redirect, get_object_or_404

from .models import Evaluation, Reviewer
from .forms import EvaluationForm, ReviewerForm


from submission.models import Submission
from institution.models import Institution



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