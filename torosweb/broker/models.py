from django.db import models


class GWGCCatalog(models.Model):
    pgc = models.IntegerField("PGC Identifier from HYPERLEDA")
    name = models.CharField("Common Name", max_length=20)
    ra = models.FloatField("Right Ascension", null=True, blank=True)
    dec = models.FloatField("Declination", null=True, blank=True)
    obj_type = models.FloatField("Type", null=True, blank=True)
    app_mag = models.FloatField("Apparent Blue Magnitude",
                                null=True, blank=True)
    maj_diam_a = models.FloatField("Major Diameter(a)", null=True, blank=True)
    err_maj_diam = models.FloatField("Error in Major Diameter",
                                     null=True, blank=True)
    min_diam_b = models.FloatField("Minor diameter (b) ",
                                   null=True, blank=True)
    err_min_diam = models.FloatField("Error in Minor diameter",
                                     null=True, blank=True)
    b_over_a = models.FloatField("b/a(Ratio of minor to major diameters) ",
                                 null=True, blank=True)
    err_b_over_a = models.FloatField("Error b/a (Ratio of minor to major"
                                     " diameters)", null=True, blank=True)
    pa = models.FloatField("Position Angle of Galaxy", null=True, blank=True)
    abs_mag = models.FloatField("Absolute Blue Magnitude",
                                null=True, blank=True)
    dist = models.FloatField("Distance", null=True, blank=True)
    err_dist = models.FloatField("Error on Distance", null=True, blank=True)
    err_app_mag = models.FloatField("Error on Apparent blue magnitude",
                                    null=True, blank=True)
    err_abs_mag = models.FloatField("Error on Absolute blue magnitude",
                                    null=True, blank=True)

    def __str__(self):
        return self.name


class Observatory(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = "observatories"


class Alert(models.Model):
    ligo_run = models.CharField("LIGO run", max_length=20)
    alert_number = models.IntegerField()
    datetime = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{0}_{1:03d}".format(self.ligo_run, self.alert_number)


class Assignment(models.Model):
    target = models.ForeignKey(GWGCCatalog)
    observatory = models.ForeignKey(Observatory)
    alert = models.ForeignKey(Alert)
    datetime = models.DateTimeField()
    is_taken = models.BooleanField(default=False)
    was_observed = models.BooleanField(default=False)

    def __str__(self):
        obs_name = self.observatory.short_name
        if obs_name is None:
            obs_name = self.observatory
        return "{} for obs {} for alert {}".format(
            self.target, obs_name, self.alert)
