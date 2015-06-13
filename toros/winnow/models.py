from django.db import models
from django.contrib.auth.models import User
import os
from stdimage.models import StdImageField

#def __get_file_path(instance, filename):
#    ext = filename.split('.')[-1]
#    filename = "%s_profilepic.%s" % (instance.user.username, ext)
#    return os.path.join('profile_images', filename)

from django.utils.deconstruct import deconstructible

@deconstructible
class GetFilePath(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        new_filename = "%s_profilepic.%s" % (instance.user.username, ext)
        return os.path.join('profile_images', new_filename)

get_file_path = GetFilePath()

class UserProfile(models.Model):
    #def __get_file_path(instance, filename):
    #    ext = filename.split('.')[-1]
    #    filename = "%s_profilepic.%s" % (instance.user.username, ext)
    #    return os.path.join('profile_images', filename)

    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    #picture = models.ImageField(upload_to=__get_file_path, blank=True)
    picture = StdImageField(upload_to=get_file_path, blank=True, 
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (200, 200),})
    fullname = models.CharField(max_length=200, blank=True)
    def save(self, *args, **kwargs):
        if self.user.first_name != "" or self.user.last_name != "":
            self.fullname = " ".join([self.user.first_name, self.user.last_name])
        super(UserProfile, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username
        
    
class TransientCandidate(models.Model):
    ra = models.FloatField()
    dec = models.FloatField()
    x_pix = models.IntegerField()
    y_pix = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    filename = models.CharField(max_length=100)
    dataset_id = models.CharField(max_length=100)
    object_id = models.IntegerField()
    slug = models.SlugField(max_length=110)
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.slug = slugify(self.dataset_id + "_%05d" % (self.object_id))
        super(TransientCandidate, self).save(*args, **kwargs)
    def __str__(self):
        return "Object %s at (%g, %g) from file: %s" % (self.object_id, self.ra, self.dec, self.filename)

    
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
    
