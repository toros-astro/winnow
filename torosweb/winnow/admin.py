from django.contrib import admin
from winnow.models import TransientCandidate, UserProfile, Ranking, Dataset

class TransientCandidateAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Sky Position", {'fields': ['ra', 'dec']}),
        ("Image Position", {'fields': ['x_pix', 'y_pix', 'width', 'height']}),
        ("File Info", {'fields': ['filename', 'dataset', 'object_id', 'slug']}),
        ("Image Files", {'fields': ['refImg', 'origImg', 'subtImg']}),
    ]
            
class RankingAdmin(admin.ModelAdmin):
    list_display = ('ranker', 'rank', 'isInteresting')

admin.site.register(UserProfile)
admin.site.register(Dataset)
admin.site.register(TransientCandidate, TransientCandidateAdmin)
admin.site.register(Ranking, RankingAdmin)
