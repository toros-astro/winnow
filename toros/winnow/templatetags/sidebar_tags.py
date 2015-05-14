from django import template
from winnow.models import Ranking, TransientCandidate, UserProfile
from django.contrib.auth.models import User
from django_comments import Comment

register = template.Library()

@register.assignment_tag
def get_top3interesting():
    #Get the top 3 interesting objects
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
    if isinstance(user, User):
        #Get userProfile instance for the user
        return UserProfile.objects.get(user=user)
    if isinstance(user, basestring):
        return UserProfile.objects.get(user=User.objects.get(username=user))
