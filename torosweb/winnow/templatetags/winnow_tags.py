from django import template
from winnow.models import Ranking, TransientCandidate, UserProfile
from django.contrib.auth.models import User
import django_comments

register = template.Library()


@register.assignment_tag
def get_top3interesting():
    # Get the top 3 interesting objects
    # This just returns 3 interesting objects
    # (it does nothing with how many likes it has)
    top3_intr = TransientCandidate.objects.\
        filter(ranking=Ranking.objects.filter(isInteresting=True)).\
        order_by('-pk')[:3]
    return top3_intr


@register.assignment_tag
def get_last3comments():
    # Get the last 3 comments
    Comment = django_comments.get_model()  # noqa
    last3_comm = Comment.objects.all().order_by('-submit_date')[:3]
    return last3_comm


@register.assignment_tag
def get_top3voters():
    # Get the top 3 voters
    top3voters = 1
    return top3voters


@register.assignment_tag
def get_userprofile(user):
    userprof = None
    if isinstance(user, User):
        # Get userProfile instance for the user
        try:
            userprof = UserProfile.objects.get(user=user)
        except:
            userprof = None
    if isinstance(user, basestring):
        try:
            userprof = UserProfile.objects.get(
                user=User.objects.get(username=user))
        except:
            userprof = None
    return userprof
