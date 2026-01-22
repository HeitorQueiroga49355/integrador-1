from django import forms
from .models import Project

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

        # Adicionando os widgets para manter as classes CSS do seu template
        widgets = {
            'campus': forms.Select(attrs={'class': 'label_form_pesquisador'}),
            'curso': forms.Select(attrs={'id': 'curso'}),
            'titulo': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Digite o título do projeto'}),
            'carga_coord': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Ex: 10 horas/semana'}),
            'inicio': forms.DateInput(attrs={'class': 'input_pesquisador', 'type': 'date'}),
            'termino': forms.DateInput(attrs={'class': 'input_pesquisador', 'type': 'date'}),
            'carga_total': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Horas totais previstas'}),
            'eixo': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Descreva o eixo temático'}),
            'interdisciplinar': forms.CheckboxInput(attrs={'class': 'input_pesquisador'}),
            'disciplinas': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Liste as disciplinas envolvidas'}),
            'cursos': forms.TextInput(attrs={'class': 'input_pesquisador completo', 'placeholder': 'Liste os cursos relacionados'}),
            'arquivo': forms.FileInput(attrs={'id': 'file-upload', 'class': 'input_pesquisador'}),
        }