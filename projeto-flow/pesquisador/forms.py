from django import forms
from .models import Project

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # Excluímos 'researcher' para não aparecer no formulário
        exclude = ['researcher']

        widgets = {
            'Institution': forms.Select(),
            'title': forms.TextInput(attrs={'placeholder': 'Digite o título do projeto'}),
            'weekly_workload': forms.NumberInput(attrs={'placeholder': 'Ex: 10'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'total_workload': forms.NumberInput(attrs={'placeholder': 'Horas totais previstas'}),
            'thematic_axis': forms.TextInput(attrs={'placeholder': 'Descreva o eixo temático'}),
            'interdisciplinary_project': forms.CheckboxInput(),
            'disciplinas': forms.TextInput(attrs={'placeholder': 'Liste as disciplinas'}),
            'courses': forms.TextInput(attrs={'placeholder': 'Liste os cursos'}),
            'project_file': forms.FileInput(attrs={'id': 'file-upload'}),
        }