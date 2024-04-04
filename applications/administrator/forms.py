from django import forms
from django.contrib.auth.models import User

class AdminUserForm(forms.ModelForm):

    tags_input_general = {
        'class': 'form-control',
    }

    username = forms.CharField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs=tags_input_general), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs=tags_input_general), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']