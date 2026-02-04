from .models import (
    Proposal,
    Version
    )
from django import forms


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['title', 'description', 'target', 'opening_date', 'closing_date', 'proposal_file', 'number_of_places']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Edital de Inovação 2024'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Regras e detalhes do edital...'}),
            'target': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Quais os objetivos deste edital?'}),
            'opening_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'closing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proposal_file': forms.FileInput(attrs={'class': 'form-control'}),
            'number_of_places': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Ex: 10'
            }),
        }
    
    def clean_number_of_places(self):
        number_of_places = self.cleaned_data.get('number_of_places')
        if number_of_places and number_of_places < 1:
            raise forms.ValidationError("O número de vagas deve ser maior que zero.")
        return number_of_places
        

class VersionProposalForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"