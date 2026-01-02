from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'researcher', 'proposal', 'proposal__title', 'status',)
    search_fields = ('proposal__title', 'status')