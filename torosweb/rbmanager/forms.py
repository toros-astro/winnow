from .models import Experiment
from django import forms


class ExperimentForm(forms.ModelForm):
    features = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': "feature1: some description, feature2, "
            "feature3, feature4: another description"}),
        required=False)

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

        def feature_set(feature_text_field):
            def parse_descriptions(astr):
                the_split = astr.split(':')
                if len(the_split) == 1:
                    return [astr.strip(), ""]
                else:
                    return [the_split[0].strip(), the_split[1].strip()]

            return [parse_descriptions(afeat)
                    for afeat in feature_text_field.split(',')]

        cleaned_data['features'] = feature_set(cleaned_data['features'])
        return cleaned_data
