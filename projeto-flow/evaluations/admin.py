from django.contrib import admin
from evaluations.models import Evaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'proposal__title', 'score', 'note_scientific_relevance', 'note_feasibility_methodological', 'note_expected_results',)
    search_fields = ('proposal__title',)
    ordering = ('score',)