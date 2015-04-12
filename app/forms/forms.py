# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Client

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
    username = forms.EmailField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Correo electrónico'}
            )
        )
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'Contraseña'}
            )
        )

    class Meta:
        fields = ['username', 'password']

class UserUpdateForm(forms.ModelForm):
    CLIENTS = (
        (0, 'Fábrica'),
        (1, 'Distribuidora'),
        (2, 'Cliente final'),
    )
    user_id = forms.IntegerField(
            required=True,
            widget=forms.HiddenInput()
        )

    client_type = forms.ChoiceField(
            label='Tipo de Cliente', 
            choices=CLIENTS, 
            widget=forms.Select( 
                    attrs={'class':'ui dropdown'}
                )
        )
    phone = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Teléfono'}
            )
        )
    address = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Dirección'}
            )
        )
    description = forms.CharField(
        required=False, 
        widget=forms.Textarea(
            attrs={'class':'form-control', 'placeholder':'descripción'}
            )
        )

    mision = forms.CharField(
        required=False, 
        widget=forms.Textarea(
            attrs={'class':'form-control', 'placeholder':'Misión'}
            )
        )

    vision = forms.CharField(
        required=False, 
        widget=forms.Textarea(
            attrs={'class':'form-control', 'placeholder':'Visión'}
            )
        )

    class Meta:
        model = Client
        fields = ("user_id", "client_type", "phone", "address", "description", "mision", "vision")

    def save(self, commit=True):
        client = super(UserUpdateForm, self).save(commit=False)
        client.user_id = self.cleaned_data["user_id"]
        if commit:
            client.save()
        return client
