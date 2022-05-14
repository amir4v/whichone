from django.contrib import admin
from . import models


admin.site.register(models.AVote)
admin.site.register(models.Option)
admin.site.register(models.Rather)