from django.contrib import admin
from .models import Proposal

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'opening_date', 'closing_date', 'is_open')
    search_fields = ('title', 'description')
    list_filter = ('opening_date', 'closing_date')
    
    def is_open(self, obj):
        return obj.is_open
    is_open.boolean = True
    is_open.short_description = 'Aberto?'