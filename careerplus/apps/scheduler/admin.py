from django.contrib import admin

from . import models


class SchedulerAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_type', 'status', 'percent_done', 'created', 'completed_on']
    raw_id_fields = ('created_by',)

admin.site.register(models.Scheduler, SchedulerAdmin)