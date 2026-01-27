from django.contrib import admin
from pesquisador.models import Researcher


@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email')

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email
