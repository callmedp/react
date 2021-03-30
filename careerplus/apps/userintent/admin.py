from django.contrib import admin

# Register your models here.

from .models import UserIntent,RecommendationFeedback

@admin.register(UserIntent)
class UserIntentAdmin(admin.ModelAdmin):
    list_display = ['intent','preferred_role','candidate_id','current_job_title','preferred_location','department','skills','experience','created']

@admin.register(RecommendationFeedback)
class RecommendationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['intent','candidate_id','recommended_products','recommendation_relevant','context','created']
