# from django import forms
#
# class PostForm(forms.Form):
#     content = forms.CharField(max_length=256)
from django import forms

class InputNumeroForm(forms.Form):

    numero = forms.IntegerField()
