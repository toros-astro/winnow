from django.forms import ModelForm
from .models import Experiment
from django import forms


class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def clean(self):
        cleaned_data = super(ExperimentForm, self).clean()
        alg_name = self.cleaned_data.get('alg_name', None)
        if alg_name is not None:
            cleaned_data['alg_name'] = alg_name.title()
            return self.cleaned_data
        return cleaned_data
