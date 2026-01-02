from .models import (
    Proposal,
    RectifyProposal
    )
from django import forms


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = "__all__"
        

class RectifyProposalForm(forms.ModelForm):
    class Meta:
        model = RectifyProposal
        fields = "__all__"