from django.contrib import admin
from . import models


class TopicChapterInline(admin.TabularInline):
    model = models.TopicChapter
    fk_name = 'topic'
    raw_id_fields = ['topic', 'chapter']
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    inlines = [TopicChapterInline]





admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Chapter)
admin.site.register(models.FAQuestion)
