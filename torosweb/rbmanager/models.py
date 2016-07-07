from django.db import models
from django.core.exceptions import ValidationError

from winnow.models import UserProfile


class Experiment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    dataset = models.ForeignKey('Dataset')
    date = models.DateField('date of experiment')
    SOFTWARE = (
        ('0', 'Weka'),
        ('1', 'RapidMiner'),
        ('2', 'scikit-learn'),
        ('3', 'Other'),
    )
    platform = models.CharField(
        'software used', max_length=1, choices=SOFTWARE, default='0')
    other_platform_name = models.CharField(max_length=20,
                                           null=True, blank=True)
    alg_name = models.CharField('algorithm name', max_length=50)
    params_file = models.FileField('parameter file name',
                                   max_length=50, null=True, blank=True)
    labels_file = models.FileField('label file name', null=True, blank=True)
    featureset_infofile = models.FileField('feature set file name',
                                           null=True, blank=True)
    featuretable_datafile = models.FileField('feature table file name',
                                             null=True, blank=True)

    conf_mat_rr = models.IntegerField('reals classified as reals')
    conf_mat_rb = models.IntegerField('reals classified as bogus')
    conf_mat_br = models.IntegerField('bogus classified as reals')
    conf_mat_bb = models.IntegerField('bogus classified as bogus')
    confusion_table_file = models.FileField(
        'confusion matrix file name', null=True, blank=True)

    other_outputfiles = models.TextField(
        'other output files', null=True, blank=True)
    other_inputfiles = models.TextField(
        'other input files', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.platform != '3':
            p_name = self.get_platform_display()
        else:
            if self.other_platform_name is None:
                p_name = "Other"
            else:
                p_name = self.other_platform_name
        return "#{}: {} in {}".format(self.id, self.alg_name, p_name)


class Dataset(models.Model):
    name = models.CharField(max_length=50)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    cadence_sec = models.FloatField(null=True, blank=True)
    subset_of = models.ForeignKey('self', null=True, blank=True)
    number_of_files = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def clean(self):
        if self.subset_of == self:
            raise ValidationError("A dataset can't be subset of itself.")

    def __str__(self):
        return self.name


# class RBUserProfile(models.Model):
#     user = models.OneToOneField(User)
#     affiliation = models.CharField(max_length=200, blank=True)
#     website = models.URLField('personal website', blank=True)
#     fullname = models.CharField(max_length=200, blank=True)
#     isDeleted = models.IntegerField(default=0)
#
#     def save(self, *args, **kwargs):
#         if self.user.first_name != "" or self.user.last_name != "":
#             self.fullname = " ".join(
#                 [self.user.first_name, self.user.last_name])
#         super(RBUserProfile, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return self.user.username
