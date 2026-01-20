from django.shortcuts import render, redirect, get_object_or_404

from .models import Evaluation
from .forms import EvaluationForm

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
