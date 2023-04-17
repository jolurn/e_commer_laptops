from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Order

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    primerNombre = forms.CharField(required=True, label='Primer nombre')
    segundoNombre = forms.CharField(required=False, label='Segundo nombre')
    apellidoPaterno = forms.CharField(required=True, label='Apellido paterno')
    apellidoMaterno = forms.CharField(required=True, label='Apellido materno')

    class Meta:
        model = CustomUser
        fields = ('email', 'primerNombre', 'segundoNombre', 'apellidoPaterno', 'apellidoMaterno', 'password1', 'password2')

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'primerNombre', 'segundoNombre', 'apellidoPaterno', 'apellidoMaterno')

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['direccion', 'ciudad', 'provincia', 'codigo_postal', 'pais']
