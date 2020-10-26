from django import forms


class UploadMdFileForm(forms.Form):
    file = forms.FileField()
