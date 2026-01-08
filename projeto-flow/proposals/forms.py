from .models import (
    Proposal,
    Version
    )
from django import forms


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = "__all__"
        

class VersionProposalForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"