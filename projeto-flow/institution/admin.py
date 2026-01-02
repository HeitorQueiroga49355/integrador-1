from django.contrib import admin
from institution.models import Institution

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'phone', 'city', 'state', 'manager')
    search_fields = ('name', 'cnpj', 'city', 'state')
    list_filter = ('state',)