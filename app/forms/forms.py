from django import forms
from app.models import User

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password")
    password2 = forms.CharField(label="Confirm Password")
    last_login = forms.DateTimeField(label="Last");

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'last_login']

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