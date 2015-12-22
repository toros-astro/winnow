from django.db import models
from django.contrib.auth.models import User
import os
from stdimage.models import StdImageField

#def __get_file_path(instance, filename):
#    ext = filename.split('.')[-1]
#    filename = "%s_profilepic.%s" % (instance.user.username, ext)
#    return os.path.join('profile_images', filename)

from django.utils.deconstruct import deconstructible

# See this SO http://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value
#and this bug report https://code.djangoproject.com/ticket/22999
@deconstructible
class GetFilePath(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        new_filename = "%s_profilepic.%s" % (instance.user.username, ext)
        return os.path.join('profile_images', new_filename)

get_file_path_for_user = GetFilePath()

class UserProfile(models.Model):
    #def __get_file_path(instance, filename):
    #    ext = filename.split('.')[-1]
    #    filename = "%s_profilepic.%s" % (instance.user.username, ext)
    #    return os.path.join('profile_images', filename)

    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    #picture = models.ImageField(upload_to=__get_file_path, blank=True)
    picture = StdImageField(upload_to=get_file_path_for_user, blank=True, null=True, 
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (200, 200),})
    fullname = models.CharField(max_length=200, blank=True)
    weight = models.FloatField(default=1.0)
    isDeleted = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if self.user.first_name != "" or self.user.last_name != "":
            self.fullname = " ".join([self.user.first_name, self.user.last_name])
        super(UserProfile, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username

@deconstructible
class GetFilePathForObject(object):
    def __init__(self, prefix):
        self.prefix = prefix
    def __call__(self, instance, filename):
        from django.utils.text import slugify
        temp_slug = slugify(instance.dataset_id + "_%05d" % (instance.object_id))
        ext = filename.split('.')[-1]
        new_filename = "%s_%s.%s" % (temp_slug, self.prefix, ext)
        return os.path.join('object_images', new_filename)


class Dataset(models.Model):
    name = models.CharField(max_length=100, unique=True)
    isCurrent = models.BooleanField(default=True)
    notes = models.TextField()
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
    dataset = models.ForeignKey(Dataset)
    object_id = models.IntegerField()
    slug = models.SlugField(max_length=110)
    refImg = StdImageField(upload_to=GetFilePathForObject("ref"),
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (400, 400),})
    origImg = StdImageField(upload_to=GetFilePathForObject("orig"),
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (400, 400),})
    subtImg = StdImageField(upload_to=GetFilePathForObject("subt"),
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (400, 400),})
    mag_orig = models.FloatField(default=0., null=True)
    mag_ref = models.FloatField(default=0., null=True)
    mag_subt = models.FloatField(default=0., null=True)
    isDeleted = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.slug = slugify(self.dataset.name + "_%05d" % (self.object_id))
        super(TransientCandidate, self).save(*args, **kwargs)
    def __str__(self):
        return "Object %s" % (self.slug)


class SEPInfo(models.Model):
    trans_candidate = models.ForeignKey(TransientCandidate)
    thresh = models.FloatField()
    npix   = models.IntegerField()
    tnpix  = models.IntegerField()
    xmin   = models.IntegerField()
    xmax   = models.IntegerField()
    ymin   = models.IntegerField()
    ymax   = models.IntegerField()
    x      = models.FloatField()
    y      = models.FloatField()
    x2     = models.FloatField()
    y2     = models.FloatField()
    xy     = models.FloatField()
    a      = models.FloatField()
    b      = models.FloatField()
    theta  = models.FloatField()
    cxx    = models.FloatField()
    cyy    = models.FloatField()
    cxy    = models.FloatField()
    cflux  = models.FloatField()
    flux   = models.FloatField()
    cpeak  = models.FloatField()
    peak   = models.FloatField()
    xcpeak = models.IntegerField()
    ycpeak = models.IntegerField()
    xpeak  = models.IntegerField()
    ypeak  = models.IntegerField()
    flag   = models.IntegerField()
    isDeleted = models.IntegerField(default=0)


class Session(models.Model):
    ranker = models.ForeignKey(UserProfile)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

  
class Ranking(models.Model):
    ranker = models.ForeignKey(UserProfile)
    trans_candidate = models.ForeignKey(TransientCandidate)
    #trans_candidate = models.IntegerField()
    #session = models.ForeignKey(Session, default=0, blank=True)
    RANKING_OPTIONS = ((-1, 'Bogus'),
                       (1, 'Real'),
                       (0, 'Unclassified'))
    rank = models.IntegerField(default=0, choices=RANKING_OPTIONS)
    isInteresting = models.BooleanField(default=False)
    #image_file = models.CharField(max_length=50, blank=True)
    #thumbnail_side = models.IntegerField(default=10, blank=True)
    isDeleted = models.IntegerField(default=0)
    def __str__(self):
        return "Ranking %d" % (self.id)
    
