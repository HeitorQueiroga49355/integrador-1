from django import forms
from .models import Evaluation, Reviewer, ReviewerInvite

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

class ReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        fields = ['name', 'email', 'cpf', 'expertise']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do avaliador'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemplo@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Inteligência Artificial, Direito Civil...'}),
        }


# Convidar um avaliador por email
class InviteForm(forms.ModelForm):
    class Meta:
        model = ReviewerInvite
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemplo@email.com'})
        }

# Formulário para o avaliador preencher (sem precisar estar logado)
class ExternalReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        fields = ['name', 'cpf', 'expertise'] # O email vai vir do convite
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control'}),
        }