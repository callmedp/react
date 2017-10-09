import logging
from django.contrib import admin
from django.contrib import messages
from .models import UserQuries
from .tasks import post_psedu_lead


# Register your models here.
def lead_creted_on_crm(modeladmin, request, queryset):

    for query in queryset:
        query_dict = {}
        try:
            usr_query = UserQuries.objects.get(id=query.id)
            query_dict.update({
                'name': usr_query.name,
                'email': usr_query.email,
                'country_code': usr_query.country.phone,
                'mobile': usr_query.phn_number,
                'message': usr_query.message,
                'source': usr_query.sourse,
                'lsource': usr_query.lead_source,
                'product': usr_query.product,
                'medium': usr_query.medium,
                'path': usr_query.path,
            })
            if not usr_query.lead_created:
                usr_query.lead_created = True
                usr_query.save()
                post_psedu_lead.delay(query_dict)
                messages.add_message(request, messages.SUCCESS, "lead created")
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
lead_creted_on_crm.short_description = 'create lead on crm'


class UserQuriesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'phn_number', 'email', 'message',
        'product', 'created',
        'lead_source', 'source'
    )
    ordering = ['-created']
    actions = [lead_creted_on_crm]
    list_per_page = 20


admin.site.register(UserQuries, UserQuriesAdmin)
