from django.contrib import admin

# Register your models here.

from .models import UserIntent

@admin.register(UserIntent)
class UserIntentAdmin(admin.ModelAdmin):
    list_display = ['intent','preferred_role','candidate_id','current_job_title','preferred_location','department','skills','experience','created']
