from django.contrib import admin
from institution.models import Institution
from address.models import Address


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cnpj',
        'email',
        'phone',
        'get_city',
        'get_state',
        'manager',
    )
    search_fields = (
        'name',
        'cnpj',
        'email',
        'address__city',
        'address__state',
    )
    list_filter = ('address__state',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'cnpj', 'phone', 'email')
        }),
        ('Endereço', {
            'fields': ('address',)
        }),
        ('Responsável', {
            'fields': ('manager',)
        }),
    )

    @admin.display(description='City')
    def get_city(self, obj):
        return obj.address.city if obj.address else '-'

    @admin.display(description='State')
    def get_state(self, obj):
        return obj.address.state if obj.address else '-'