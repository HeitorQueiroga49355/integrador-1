from django.contrib import admin
from user.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'get_city', 'get_state')

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description='City')
    def get_city(self, obj):
        return obj.address.city if obj.address else '-'

    @admin.display(description='State')
    def get_state(self, obj):
        return obj.address.state if obj.address else '-'
