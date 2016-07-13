from django.db import models

from winnow.models import UserProfile, Dataset


class Experiment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset)
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

    features = models.ManyToManyField('Feature')
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

    class Meta:
        ordering = ('-date',)


class Feature(models.Model):
    name = models.CharField(max_length=20)
    code = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
