from django.contrib import admin
from .models import Observatory, Assignment, Alert
# Register your models here.

admin.site.register(Observatory)
admin.site.register(Assignment)
admin.site.register(Alert)
