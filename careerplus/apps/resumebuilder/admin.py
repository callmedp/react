from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Candidate)

admin.site.register(OrderCustomisation)


class CandidateResumeOperationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'op_status', )


admin.site.register(CandidateResumeOperations, CandidateResumeOperationAdmin)