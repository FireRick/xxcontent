from django import forms


class DescAdminForm(forms.ModelForm):
    """
    将各 model 的 desc 字段的 widget 改为 Textarea
    若特定 model 需要定制特殊的 widget，可以以这个为父类继承后在该 model 中引入
    """
    desc = forms.CharField(widget=forms.Textarea)