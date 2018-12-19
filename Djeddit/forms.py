from django import forms

class SubredditForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.Charfield(max_length=500)