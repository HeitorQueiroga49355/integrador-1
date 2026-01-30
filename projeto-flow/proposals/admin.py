from django.contrib import admin
from .models import Proposal

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'institution', 'opening_date', 'closing_date')
    search_fields = ('title', 'institution__name')