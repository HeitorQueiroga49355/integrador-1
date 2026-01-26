from dataclasses import fields
from django import forms
from .models import Project

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        
        # Exclui 'researcher' e 'proposal' para não aparecerem no formulário

        exclude = ['researcher', 'proposal']

        widgets = {
            'Institution': forms.Select(attrs={'class': 'input_pesquisador'}),
            'title': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Digite o título do projeto', 'id': 'titulo'}),
            'course': forms.Select(attrs={'class': 'input_pesquisador'}),
            'weekly_workload': forms.NumberInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Ex: 10 horas/semana', 'id': 'carga-coord'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'total_workload': forms.NumberInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Horas totais previstas'}),
            'thematic_axis': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Descreva o eixo temático'}),
            'interdisciplinary_project': forms.CheckboxInput(attrs={'class': 'input_pesquisador','name': 'interdisciplinary_project'}),
            'disciplines': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Liste as disciplinas'}),
            'courses': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Liste os cursos'}),
            'project_file': forms.FileInput(attrs={'class=':'input_pesquisador', 'id':"file-upload", 'type':'file', 'aria-hidden':"true",'id': 'file-upload'}),
        }