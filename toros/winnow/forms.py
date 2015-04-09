from django import forms
from winnow.models import Ranking

class RankingForm(forms.ModelForm):
    RANKING_OPTIONS = (('B', 'Bogus'),
                       ('R', 'Real'),
                       ('X', 'Unclassified'))
    rank = forms.ChoiceField(choices=RANKING_OPTIONS, widget=forms.RadioSelect)
    isInteresting = forms.BooleanField(help_text = 'Mark as interesting', initial=False, required=False)
    trans_candidate = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    
    class Meta:
        model = Ranking
        fields = ('rank', 'isInteresting', 'trans_candidate')
