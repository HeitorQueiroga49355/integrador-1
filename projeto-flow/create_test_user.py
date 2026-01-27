#!/usr/bin/env python
"""
Script para criar um usuário de teste
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from user.models import User, Profile

# Verifica se já existe um usuário de teste
email = "teste@exemplo.com"
username = "teste"

try:
    user = User.objects.get(email=email)
    print(f"✓ Usuário de teste já existe: {user.email}")
except User.DoesNotExist:
    # Criar usuário de teste
    user = User.objects.create_user(
        username=username,
        email=email,
        password="senha123",
        first_name="Usuário",
        last_name="Teste"
    )

    # Criar perfil para o usuário
    profile = Profile.objects.create(
        user=user,
        role=Profile.Role.RESEARCHER
    )

    print("=" * 60)
    print("✓ Usuário de teste criado com sucesso!")
    print("=" * 60)
    print(f"Email:    {email}")
    print(f"Senha:    senha123")
    print(f"Nome:     {user.first_name} {user.last_name}")
    print(f"Perfil:   {profile.get_role_display()}")
    print("=" * 60)
