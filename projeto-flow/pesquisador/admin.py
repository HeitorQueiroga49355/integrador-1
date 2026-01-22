from django.contrib import admin
from pesquisador.models import Researcher, Project
from user.models import Profile


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

# @admin.register(Profile)

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'get_email', 'get_city', 'get_state')

#     @admin.display(description='Email')
#     def get_email(self, obj):
#         return obj.user.email

#     @admin.display(description='City')
#     def get_city(self, obj):
#         return obj.address.city if obj.address else '-'

#     @admin.display(description='State')
#     def get_state(self, obj):
#         return obj.address.state if obj.address else '-'

