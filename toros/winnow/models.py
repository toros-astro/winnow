from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=200)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.name
        
    
class TransientCandidate(models.Model):
    ra = models.FloatField()
    dec = models.FloatField()
    x_pix = models.IntegerField()
    y_pix = models.IntegerField()
    sigma_x = models.IntegerField()
    sigma_y = models.IntegerField()
    neg_pix_fraction = models.FloatField()
    #Add the image where this comes from!!!
    def __str__(self):
        return "Object at (%g, %g)" % (self.ra, self.dec)

    
class Session(models.Model):
    ranker = models.ForeignKey(User)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

  
class Ranking(models.Model):
    ranker = models.ForeignKey(User)
    #trans_candidate = models.ForeignKey(TransientCandidate, blank=True)
    trans_candidate = models.IntegerField()
    #session = models.ForeignKey(Session, default=0, blank=True)
    RANKING_OPTIONS = (('B', 'Bogus'),
                       ('R', 'Real'),
                       ('X', 'Unclassified'))
    rank = models.CharField(max_length=1, choices=RANKING_OPTIONS)
    isInteresting = models.BooleanField(default=False)
    #image_file = models.CharField(max_length=50, blank=True)
    #thumbnail_side = models.IntegerField(default=10, blank=True)
    def __str__(self):
        return "Ranking %d" % (self.id)
    
