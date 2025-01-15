import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from . import models

class ContactForm(forms.ModelForm):



  first_name = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Digite o nome aqui',
      }
    ),label= 'Nome'
  )

  last_name = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Digite o sobrenome aqui',
      }
    ),label= 'Sobrenome'
  )

  phone = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Digite o telefone aqui',
      }
    ),label= 'Telefone'
  )
  
  picture = forms.ImageField(
    widget=forms.FileInput(
      attrs={
        'accept':'image/*',
      }
    )
  )


  class Meta: 
    model = models.Contact
    fields = 'first_name', 'last_name', 'phone','email','description','category', 'picture'
    
    
  def clean(self):
    cleaned_data = self.cleaned_data
    first_name = cleaned_data.get('first_name')
    last_name = cleaned_data.get('last_name')

    if first_name == last_name:
      msg = ValidationError(
          'Nome não pode ser igual a Sobrenome',
          code = 'invalid'
        )
      
      self.add_error('first_name',msg)
      self.add_error('last_name',msg)
    # para validações com campos multiplos, por exemplo validação entre nome e sobrenome ou
    # validação de senhas iguais, deve se usar a def clean com retorno de "super().clean()"
    return super().clean()

  def clean_first_name(self):
    first_name = cleaned_data = self.cleaned_data.get('first_name')
    
    if first_name and re.search(r'\d', first_name):
      self.add_error(
        'first_name',
        ValidationError(
          'Nome não pode conter um número',
          code='invalid'
        )
      )
    # para validações de um único campo, deve se usar de clean_'nome_do_campo' e retornar o campo
    # como mostrado abaixo:
    return first_name
  
  def clean_last_name(self):
    last_name = cleaned_data = self.cleaned_data.get('last_name')
    
    if last_name and re.search(r'\d', last_name):
      self.add_error(
        'last_name',
        ValidationError(
          'Sobrenome não pode conter um número',
          code='invalid'
        )
      )
    # para validações de um único campo, deve se usar de clean_'nome_do_campo' e retornar o campo
    # como mostrado abaixo:
    return last_name

class RegisterForm(UserCreationForm):
  first_name = forms.CharField(
    required=True,
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Informe seu nome',
      }
    ),label= 'Nome'
  )

  last_name = forms.CharField(
    required=True,
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Informe seu sobrenome',
      }
    ),label= 'Sobrenome'
  )
  
  email = forms.EmailField(
    required=True,
    widget=forms.TextInput(
      attrs={
        'placeholder': 'Informe seu E-mail',
      }
    ),label= 'E-mail'
  )


  class Meta:
    model = User
    fields = (
      'first_name', 'last_name', 'email', 
      'username', 'password1', 'password2',
    )

  def clean_email(self):
    email = self.cleaned_data.get('email')

    if User.objects.filter(email=email).exists():
      self.add_error(
        'email',
        ValidationError('Email já existe')
      )

    return email
  

class RegisterUpdateForm(forms.ModelForm):
  first_name = forms.CharField(
    min_length=2,
    max_length=30,
    required=True,
    help_text= 'Required.',
    error_messages={
      'min_lenght': 'Nome muito pequeno'
    }
  )
  last_name = forms.CharField(
    min_length=2,
    max_length=30,
    required=True,
    help_text= 'Required.',
  )
  password1 = forms.CharField(
    label="Senha",
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
    help_text=password_validation.password_validators_help_text_html(),
    required=False,
  )
  password2 = forms.CharField(
    label="Confirmar senha",
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
    help_text='Senha não é igual a anterior',
    required=False,
  )

  def clean_email(self):
    email = self.cleaned_data.get('email')
    current_email = self.instance.email

    if current_email != email:

      if User.objects.filter(email=email).exists():
        self.add_error(
          'email',
          ValidationError('Email já existe')
        )

    return email
  
  def save(self, commit=True):
    cleaned_data = self.cleaned_data
    user = super().save(commit=False)

    password = cleaned_data.get('password1')

    if password:
      user.set_password(password)

    if commit:
      user.save()

    return user

  def clean(self):
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    
    if password1 or password2:
      if password1 != password2:
        self.add_error(
          'password2',
          ValidationError('Senhas não batem'),
        )
    return super().clean()


  def clean_password1(self):
    password1 = self.cleaned_data.get('password1')

    if password1:
      try:
        password_validation.validate_password(password1)
      except ValidationError as errors:
        self.add_error(
          'password1',
          ValidationError(errors)
        )

    return password1

  class Meta:
    model = User
    fields = (
      'first_name', 'last_name', 'email', 
      'username',
    )