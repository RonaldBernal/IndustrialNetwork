# -*- coding: utf-8 -*-
from django import forms
#from app.models import Client
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(forms.ModelForm):
    username = forms.EmailField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Correo electrónico'}
            )
        )
    first_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Nombre del encargado'}
            )
        )
    last_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Apellido del encargado'}
            )
        )
    password1 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'Contraseña'}
            )
        )
    password2 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'Confirmar contraseña'}
            )
        )
    email = forms.EmailField(
        required=True, 
        widget=forms.HiddenInput(attrs={'value':''}
            )
        )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    username = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['username', 'password']
'''
class RegistrationForm(forms.ModelForm):

    CLIENTS = (
        (0, 'Fábrica'),
        (1, 'Distribuidora'),
        (2, 'Cliente final'),
    )

    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la empresa'}))
    client_type = forms.ChoiceField(label='Tipo de Cliente', choices=CLIENTS, widget=forms.Select(attrs={'class':'form-control'}))
    username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo electrónico'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirmar contraseña'}))
    last_login = forms.DateTimeField(label="Last", widget=forms.HiddenInput(attrs={'value':''}));

    class Meta:
        model = CUser
        fields = ['name', 'client_type', 'username', 'password1', 'password2', 'last_login']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user
'''