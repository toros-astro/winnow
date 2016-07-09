from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from stdimage.models import StdImageField

import os
import math

# def __get_file_path(instance, filename):
#    ext = filename.split('.')[-1]
#    filename = "%s_profilepic.%s" % (instance.user.username, ext)
#    return os.path.join('profile_images', filename)

from django.utils.deconstruct import deconstructible


# See this SO http://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value
# and this bug report https://code.djangoproject.com/ticket/22999
@deconstructible
class GetFilePath(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        new_filename = "%s_profilepic.%s" % (instance.user.username, ext)
        return os.path.join('profile_images', new_filename)

get_file_path_for_user = GetFilePath()


class UserProfile(models.Model):
    # def __get_file_path(instance, filename):
    #    ext = filename.split('.')[-1]
    #    filename = "%s_profilepic.%s" % (instance.user.username, ext)
    #    return os.path.join('profile_images', filename)

    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    # picture = models.ImageField(upload_to=__get_file_path, blank=True)
    picture = StdImageField(upload_to=get_file_path_for_user,
                            blank=True, null=True,
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (200, 200), })
    fullname = models.CharField(max_length=200, blank=True)
    weight = models.FloatField(default=1.0)
    isDeleted = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.user.first_name != "" or self.user.last_name != "":
            self.fullname = " ".join(
                [self.user.first_name, self.user.last_name])
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


@deconstructible
class GetFilePathForObject(object):
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, instance, filename):
        from django.utils.text import slugify
        temp_slug = slugify(
            instance.dataset_id + "_%05d" % (instance.object_id))
        ext = filename.split('.')[-1]
        new_filename = "%s_%s.%s" % (temp_slug, self.prefix, ext)
        return os.path.join('object_images', new_filename)


class Dataset(models.Model):
    name = models.CharField(max_length=100, unique=True)
    isCurrent = models.BooleanField(default=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    cadence_sec = models.FloatField(null=True, blank=True)
    subset_of = models.ForeignKey('self', null=True, blank=True)
    number_of_files = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def number_of_reals(self):
        from django.db.models import Sum
        tc_query = TransientCandidate.objects.filter(dataset=self)
        num_reals = tc_query.annotate(brclass=Sum('ranking__rank')).\
            filter(brclass__gt=0).count()
        return num_reals

    def number_of_bogus(self):
        from django.db.models import Sum
        tc_query = TransientCandidate.objects.filter(dataset=self)
        num_bogus = tc_query.annotate(brclass=Sum('ranking__rank')).\
            filter(brclass__lt=0).count()
        return num_bogus

    def number_of_unclassified(self):
        from django.db.models import Sum
        tc_query = TransientCandidate.objects.filter(dataset=self)
        num_unclassified = tc_query.annotate(brclass=Sum('ranking__rank')).\
            filter(brclass__exact=0).count()
        return num_unclassified

    def number_not_ranked(self):
        not_ranked = TransientCandidate.objects.filter(dataset=self).\
            exclude(ranking=Ranking.objects.all()).count()
        return not_ranked

    def number_of_objects(self):
        return TransientCandidate.objects.filter(dataset=self).count()

    def number_of_rbx(self):
        from django.db.models import Sum
        tc_query = TransientCandidate.objects.filter(dataset=self)
        num_reals = tc_query.annotate(brclass=Sum('ranking__rank')).\
            filter(brclass__gt=0).count()
        num_bogus = tc_query.annotate(brclass=Sum('ranking__rank')).\
            filter(brclass__lt=0).count()
        total = tc_query.count()
        num_no_label = total - (num_reals + num_bogus)
        return num_reals, num_bogus, num_no_label

    def clean(self):
        if self.subset_of == self:
            raise ValidationError("A dataset can't be subset of itself.")

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
                                       'normal': (400, 400), })
    origImg = StdImageField(upload_to=GetFilePathForObject("orig"),
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (400, 400), })
    subtImg = StdImageField(upload_to=GetFilePathForObject("subt"),
                            variations={'thumbnail': (50, 50, True),
                                        'normal': (400, 400), })
    mag_orig = models.FloatField(default=0., null=True)
    mag_ref = models.FloatField(default=0., null=True)
    mag_subt = models.FloatField(default=0., null=True)
    isDeleted = models.IntegerField(default=0)

    def aladin_coords(self):
        ra = self.ra
        dec = self.dec
        ra_deg = int(ra)
        ra_min = int((ra - ra_deg) * 60.)
        dec_deg = int(dec)
        dec_min = abs(int((dec - dec_deg) * 60.))
        sgn = "+" if dec > 0 else ""
        return "%d %02d %s%02d %02d" % (ra_deg, ra_min, sgn, dec_deg, dec_min)

    def number_of_real_votes(self):
        num_real = Ranking.objects.filter(trans_candidate=self).\
            filter(rank=1).count()
        return num_real

    def number_of_bogus_votes(self):
        num_bogus = Ranking.objects.filter(trans_candidate=self).\
            filter(rank=-1).count()
        return num_bogus

    def number_of_unclassified_votes(self):
        num_unclassifed = Ranking.objects.filter(trans_candidate=self).\
            filter(rank=0).count()
        return num_unclassifed

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.slug = slugify(self.dataset.name + "_%05d" % (self.object_id))
        super(TransientCandidate, self).save(*args, **kwargs)

    def __str__(self):
        return "Object %s at (%g, %g) from file: %s" % \
            (self.slug, self.ra, self.dec, self.filename)


class SEPInfo(models.Model):
    trans_candidate = models.OneToOneField(TransientCandidate)
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

    def fwhm_x(self):
        return 2 * math.sqrt(2. * math.log(2.) * self.x2)

    def fwhm_y(self):
        return 2 * math.sqrt(2. * math.log(2.) * self.y2)

    def flag_labels(self):
        flags = []
        if (self.flag & 1) != 0:
            flags.append('Object is result of deblending')
        if (self.flag & 2) != 0:
            flags.append('Object is truncated at image boundary')
        if (self.flag & 8) != 0:
            flags.append('x, y fully correlated in object')
        if (self.flag & 16) != 0:
            flags.append('Aperture truncated at image boundary')
        if (self.flag & 32) != 0:
            flags.append('Aperture contains one or more masked pixels')
        if (self.flag & 64) != 0:
            flags.append('Aperture contains only masked pixels')
        if (self.flag & 128) != 0:
            flags.append('Aperture sum is negative in kron_radius')
        return flags


class Session(models.Model):
    ranker = models.ForeignKey(UserProfile)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()


class Ranking(models.Model):
    ranker = models.ForeignKey(UserProfile)
    trans_candidate = models.ForeignKey(TransientCandidate)
    # trans_candidate = models.IntegerField()
    # session = models.ForeignKey(Session, default=0, blank=True)
    RANKING_OPTIONS = ((-1, 'Bogus'),
                       (1, 'Real'),
                       (0, 'Unclassified'))
    rank = models.IntegerField(default=0, choices=RANKING_OPTIONS)
    isInteresting = models.BooleanField(default=False)
    # image_file = models.CharField(max_length=50, blank=True)
    # thumbnail_side = models.IntegerField(default=10, blank=True)
    isDeleted = models.IntegerField(default=0)

    def __str__(self):
        return "Ranking %d" % (self.id)
