from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=200)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    name = models.CharField(max_length=200)
    def save(self, *args, **kwargs):
        self.name = " ".join([self.user.first_name, self.user.last_name])
        super(UserProfile, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
        
    
class TransientCandidate(models.Model):
    ra = models.FloatField()
    dec = models.FloatField()
    x_pix = models.IntegerField()
    y_pix = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    filename = models.CharField(max_length=100)
    def __str__(self):
        return "Object at (%g, %g) from file: %s" % (self.ra, self.dec, self.filename)

    
class Session(models.Model):
    ranker = models.ForeignKey(UserProfile)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

  
class Ranking(models.Model):
    ranker = models.ForeignKey(UserProfile)
    trans_candidate = models.ForeignKey(TransientCandidate)
    #trans_candidate = models.IntegerField()
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
    
