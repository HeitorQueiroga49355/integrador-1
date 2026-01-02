from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cpf', 'phone', 'city', 'role')
    search_fields = ('user__username', 'cpf', 'phone', 'city')