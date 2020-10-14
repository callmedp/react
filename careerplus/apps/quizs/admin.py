from django.contrib import admin
from . models import QuizResponse


# Register your models here.
class QuizResponseAdmin(admin.ModelAdmin):
    model = QuizResponse
    raw_id_fields = ('oi',)
    search_fields = ('oi',)
    ordering = ('-created_on',)


admin.site.register(QuizResponse, QuizResponseAdmin)
