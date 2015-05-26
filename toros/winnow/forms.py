from django import forms
from winnow.models import Ranking, UserProfile
from django.contrib.auth.models import User

class RankingForm(forms.ModelForm):
    RANKING_OPTIONS = (('B', 'Bogus'),
                       ('R', 'Real'),
                       ('X', 'Unclassified'))
    rank = forms.ChoiceField(choices=RANKING_OPTIONS, widget=forms.RadioSelect, help_text="Options")
    isInteresting = forms.BooleanField(help_text = 'Mark as interesting', initial=False, required=False)
    #trans_candidate = forms.ForeignKey(widget=forms.HiddenInput())
    
    class Meta:
        model = Ranking
        fields = ('rank', 'isInteresting') #, 'trans_candidate')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['repeat_password']:
            self._errors['password'] = ["Passwords do not match"] # Will raise a error message
            del form_data['password']
        return form_data
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'repeat_password')

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(label='Personal website', required=False)
    picture = forms.ImageField(label='Profile picture', required=False)
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
