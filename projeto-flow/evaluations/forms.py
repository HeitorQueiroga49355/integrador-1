from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'note_scientific_relevance',
            'note_feasibility_methodological',
            'note_expected_results',
            'project_report',
            'strength_points',
            'weak_points',
            'recommendations'
        ]
        
        widgets = {
            'note_scientific_relevance': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'placeholder': '0-10'}),
            'note_feasibility_methodological': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'placeholder': '0-10'}),
            'note_expected_results': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'placeholder': '0-10'}),
            
            'project_report': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Insira o relatório detalhado...'}),
            'strength_points': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Destaque os pontos positivos...'}),
            'weak_points': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Aponte as fragilidades...'}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Sugestões para melhoria...'}),
        }