from .models import Proposal
from django import forms

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['title', 'description', 'departament', 'proprsal_file']