from django import forms
from winnow.models import Ranking

class RankingForm(forms.ModelForm):
    RANKING_OPTIONS = (('B', 'Bogus'),
                       ('R', 'Real'),
                       ('X', 'Unclassified'))
    rank = forms.ChoiceField(choices=RANKING_OPTIONS, widget=forms.RadioSelect, help_text="Transient classification")
    isInteresting = forms.BooleanField(help_text = 'Mark as interesting', initial=False, required=False)
    #trans_candidate = forms.ForeignKey(widget=forms.HiddenInput())
    
    class Meta:
        model = Ranking
        fields = ('rank', 'isInteresting') #, 'trans_candidate')
