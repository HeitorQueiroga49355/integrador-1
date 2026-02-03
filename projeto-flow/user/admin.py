from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile

# Inline para Profile no UserAdmin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'

# UserAdmin customizado com Profile inline
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    # Adiciona os campos personalizados ao formulário
    fieldsets = UserAdmin.fieldsets + (
        (_('Informações pessoais'), {
            'fields': ('cpf', 'phone', 'address')
        }),
    )
    
    # Adiciona os campos personalizados à listagem
    list_display = ('username', 'email', 'cpf', 'phone', 'get_role', 'is_staff')
    search_fields = ('username', 'email', 'cpf', 'profile__role')
    
    @admin.display(description='Cargo')
    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else '-'

# ProfileAdmin mantido para visualização separada
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'get_email', 'get_city', 'get_state')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'role')
    
    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email
    
    @admin.display(description='City')
    def get_city(self, obj):
        return obj.user.address.city if obj.user.address else '-'
    
    @admin.display(description='State')
    def get_state(self, obj):
        return obj.user.address.state if obj.user.address else '-'