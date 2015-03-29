# -*- coding: utf-8 -*-
from django import forms
from app.models import User
from datetime import datetime

class RegistrationForm(forms.ModelForm):

    CLIENTS = (
        (0, 'Fábrica'),
        (1, 'Distribuidora'),
        (2, 'Cliente final'),
    )

    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la empresa'}))
    client_type = forms.ChoiceField(label='Tipo de Cliente', choices=CLIENTS, widget=forms.Select(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo electrónico'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirmar contraseña'}))
    last_login = forms.DateTimeField(label="Last", widget=forms.HiddenInput(attrs={'value':''}));

    class Meta:
        model = User
        fields = ['name', 'client_type', 'email', 'password1', 'password2', 'last_login']

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

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']