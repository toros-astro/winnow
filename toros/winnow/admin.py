from django.contrib import admin
from winnow.models import TransientCandidate, UserProfile, Ranking

class TransientCandidateAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Sky Position", {'fields': ['ra', 'dec']}),
        ("Image Position", {'fields': ['x_pix', 'y_pix']}),
        ("Second Moments", {'fields': ['sigma_x', 'sigma_y']}),
        (None, {'fields': ['neg_pix_fraction']})
    ]            
            
class RankingAdmin(admin.ModelAdmin):
    list_display = ('ranker', 'rank', 'isInteresting')

admin.site.register(UserProfile)
admin.site.register(TransientCandidate, TransientCandidateAdmin)
admin.site.register(Ranking, RankingAdmin)