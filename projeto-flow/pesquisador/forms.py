from django import forms
from submission.models import Submission

class CreateSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        # Inclua os campos que o pesquisador deve preencher
        fields = [
            'title', 'keywords', 'abstract', 'justification', 'methodology',
            'project_timeline', 'project_budget', 'expected_results', 'submission_file'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input_pesquisador completo'}),
            'keywords': forms.TextInput(attrs={'class': 'input_pesquisador completo'}),
            'abstract': forms.Textarea(attrs={'class': 'input_pesquisador completo', 'rows': 4}),
            'justification': forms.Textarea(attrs={'class': 'input_pesquisador completo', 'rows': 4}),
            'methodology': forms.Textarea(attrs={'class': 'input_pesquisador completo', 'rows': 4}),
            'project_timeline': forms.Textarea(attrs={'class': 'input_pesquisador completo', 'rows': 4}),
            'project_budget': forms.Textarea(attrs={'class': 'input_pesquisador completo', 'rows': 4}),
            'expected_results': forms.Textarea(attrs={'class': 'input_pesquisador completo', 'rows': 4}),
            'submission_file': forms.ClearableFileInput(attrs={'class': 'input_pesquisador completo'}),
        }
