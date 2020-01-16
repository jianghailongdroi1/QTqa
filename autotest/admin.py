from django.contrib import admin
from autotest import models
# Register your models here.

# class ProjectAdmin(models.models):

admin.site.register(models.Project)
admin.site.register(models.CronJob)
admin.site.register(models.Job_result)
admin.site.register(models.Subtask)
admin.site.register(models.suite)