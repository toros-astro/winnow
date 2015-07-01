from django import template
from winnow.models import Ranking, TransientCandidate, UserProfile, SEPInfo
from django.contrib.auth.models import User
from django_comments import Comment
import numpy as np

register = template.Library()

@register.assignment_tag
def get_top3interesting():
    #Get the top 3 interesting objects
    #This just returns 3 interesting objects (it does nothing with how many likes it has)
    top3_intr = TransientCandidate.objects.filter(ranking=Ranking.objects.filter(isInteresting = True))[:3]
    return top3_intr

@register.assignment_tag
def get_last3comments():
    #Get the last 3 comments
    last3_comm = Comment.objects.all().order_by('-submit_date')[:3]
    return last3_comm

@register.assignment_tag
def get_top3voters():
    #Get the top 3 voters
    top3voters = 1
    return top3voters

@register.assignment_tag
def get_userprofile(user):
    userprof = None
    if isinstance(user, User):
        #Get userProfile instance for the user
        try:
            userprof = UserProfile.objects.get(user=user)
        except:
            userprof = None
    if isinstance(user, basestring):
        try:
            userprof = UserProfile.objects.get(user=User.objects.get(username=user))
        except:
            userprof = None
    return userprof

@register.assignment_tag
def get_votes_for_object(object_id):
    tc = TransientCandidate.objects.get(pk = object_id)
    num_real = Ranking.objects.filter(trans_candidate=tc).filter(rank='R').count()
    num_bogus = Ranking.objects.filter(trans_candidate=tc).filter(rank='B').count()
    num_unclassf = Ranking.objects.filter(trans_candidate=tc).filter(rank='X').count()
    return {'real':num_real, 'bogus':num_bogus, 'unknown':num_unclassf}
    
@register.assignment_tag
def get_profile_stats(auserprofile):
    num_rankings = Ranking.objects.filter(ranker=auserprofile).count()
    int_objects = TransientCandidate.objects.filter(ranking=Ranking.objects.filter(ranker=auserprofile).filter(isInteresting=True))
    latestComments = Comment.objects.filter(user=auserprofile.user)
    return {'num_rankings': num_rankings, 'int_objects': int_objects, 'latestComments': latestComments}

@register.assignment_tag
def get_sep_info(object_slug):
    try:
        the_object = TransientCandidate.objects.get(slug = object_slug)
        sep = SEPInfo.objects.get(trans_candidate = the_object)
        fwhm_x = 2*np.sqrt(2.*np.log(2.)*sep.x2)
        fwhm_y = 2*np.sqrt(2.*np.log(2.)*sep.y2)
        sep_extra = {'fwhm_x': fwhm_x, 'fwhm_y': fwhm_y}
        flags = []
        if (sep.flag & 1) != 0:
            flags.append('Object is result of deblending')
        if (sep.flag & 2) != 0:
            flags.append('Object is truncated at image boundary')
        if (sep.flag & 8) != 0:
            flags.append('x, y fully correlated in object')
        if (sep.flag & 16) != 0:
            flags.append('Aperture truncated at image boundary')
        if (sep.flag & 32) != 0:
            flags.append('Aperture contains one or more masked pixels')
        if (sep.flag & 64) != 0:
            flags.append('Aperture contains only masked pixels')
        if (sep.flag & 128) != 0:
            flags.append('Aperture sum is negative in kron_radius')
        sep_extra['flags'] = flags
    except:
        sep = None
        sep_extra = None
    return {'sep': sep, 'sep_extra': sep_extra}









