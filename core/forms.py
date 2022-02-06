from django import forms

from .models import EstimateRequest


class EstimateRequestForm(forms.ModelForm):

    class Meta:
        model = EstimateRequest
        fields = ['full_name', 'email', 'url']
