from django.contrib import admin
from pesquisador.models import Researcher, Project


@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email')

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'researcher', 'start_date', 'end_date')

    @admin.display(description='Pesquisador')
    def get_researcher(self, obj):
        return obj.researcher.user.username