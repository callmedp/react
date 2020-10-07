from django.contrib import admin
from . import models
from .choices import SECTION_MAPPING

class ResumeScoreCheckerAdmin(admin.ModelAdmin):
    model = models.ResumeScoreCheckerUserDetails
    list_display = ('email', 'mobile_number', 'candidate_id', 'total_score', 'section_scores_list',)

    def section_scores_list(self, obj):
        section_text = ''
        for key in obj.section_scores:
            section_text += SECTION_MAPPING[key] + " : " + obj.section_scores[key] + ', '
        return section_text

admin.site.register(models.ResumeScoreCheckerUserDetails, ResumeScoreCheckerAdmin)
