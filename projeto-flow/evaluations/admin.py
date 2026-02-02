from django.contrib import admin
from .models import Evaluation, Reviewer, ReviewerInvite

@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'expertise', 'institution')
    search_fields = ('name', 'email', 'cpf')
    list_filter = ('institution',)

@admin.register(ReviewerInvite)
class ReviewerInviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'accepted', 'created_at')
    list_filter = ('accepted', 'created_at')
    search_fields = ('email',)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('submission', 'score', 'created_at')
    list_filter = ('score',)
    search_fields = ('submission__title',)
    raw_id_fields = ('submission', 'institution', 'proposal')