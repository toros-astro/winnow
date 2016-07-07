from django.contrib import admin
from .models import Experiment, Dataset


admin.site.register(Experiment)
admin.site.register(Dataset)
