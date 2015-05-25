from django import template
from winnow.models import Ranking, TransientCandidate, UserProfile
from django.contrib.auth.models import User
from django_comments import Comment

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
    latest3Comments = Comment.objects.filter(user=auserprofile.user)[:3]
    return {'num_rankings': num_rankings, 'int_objects': int_objects, 'latest3Comments': latest3Comments}
    
    
    
    