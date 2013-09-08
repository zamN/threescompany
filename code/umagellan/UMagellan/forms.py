from django import forms

class UserForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
    first_name = forms.CharField()
    last_name = forms.CharField()