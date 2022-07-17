
from django import forms
from .models import Rweets


class RweetForm(forms.ModelForm):
    body = forms.CharField(required=True, 
    widget=forms.widgets.Textarea(
        attrs={
        'placeholder': 'Rweet something....',
        'class': 'textarea is-success is-medium',
            }
        ),
        label=''
    )

    class Meta:
        model = Rweets
        exclude = ("user", )