from django import forms


class SubredditForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())