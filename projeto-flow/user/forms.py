from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira seu e-mail',
            'id': 'emailInput'
        }),
        label='E-mail'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira sua senha',
            'id': 'senhaInput'
        }),
        label='Senha'
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'loginForm-bottomButtons__rememberLabel__checkbox',
            'id': 'rememberMeInput'
        }),
        label='Lembre-me'
    )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira seu nome',
            'id': 'nameInput'
        }),
        label='Nome'
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira seu sobrenome',
            'id': 'sobrenomeInput'
        }),
        label='Sobrenome'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira seu e-mail',
            'id': 'emailInput'
        }),
        label='E-mail'
    )
    cpf = forms.CharField(
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira seu CPF (apenas números)',
            'id': 'cpfInput',
            'pattern': '[0-9]{11}'
        }),
        label='CPF'
    )
    phone = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira seu telefone',
            'id': 'phoneInput'
        }),
        label='Telefone'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Insira sua senha',
            'id': 'password1Input'
        }),
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'loginForm-label__input',
            'placeholder': 'Confirme sua senha',
            'id': 'password2Input'
        }),
        label='Confirmar Senha'
    )
    role = forms.ChoiceField(
        choices=[
            ('researcher', 'Pesquisador'),
            ('manager', 'Gerente'),
            ('evaluator', 'Avaliador'),
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'loginForm-label__input',
            'id': 'roleInput'
        }),
        label='Tipo de Usuário'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'cpf', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and User.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username
        user.cpf = self.cleaned_data.get('cpf')
        user.phone = self.cleaned_data.get('phone')

        if commit:
            user.save()
            # Create profile
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user
