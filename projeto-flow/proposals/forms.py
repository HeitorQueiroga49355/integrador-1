from .models import (
    Proposal,
    RectifyProposal
    )
from django import forms

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['title', 'description', 'departament', 'proprsal_file']
        

class RectifyProposalForm(forms.ModelForm):
    class Meta:
        model = RectifyProposal
        fields = ['title', 'description', 'departament', 'rectify_file']