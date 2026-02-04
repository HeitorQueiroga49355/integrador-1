from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'
    max_num = 1


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'cpf', 'phone', 'address')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    list_display = ('username', 'email', 'cpf', 'phone', 'get_role', 'is_staff')
    search_fields = ('username', 'email', 'cpf', 'profile__role')
    
    @admin.display(description='Cargo')
    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else '-'

    def get_inline_instances(self, request, obj=None):
        """Garante que o ProfileInline só aparece quando edita um usuário existente"""
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'get_email', 'get_city', 'get_state')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'role')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'role')
        }),
        ('Foto de Perfil', {
            'fields': ('profile_picture',),
            'description': _('Formatos: JPG, JPEG, PNG, GIF, WEBP, BMP. Tamanho máximo: 5MB.')
        }),
    )
    
    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email
    
    @admin.display(description='City')
    def get_city(self, obj):
        return obj.user.address.city if obj.user.address else '-'
    
    @admin.display(description='State')
    def get_state(self, obj):
        return obj.user.address.state if obj.user.address else '-'