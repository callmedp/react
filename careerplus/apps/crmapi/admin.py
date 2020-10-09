import logging
from django.contrib import admin
from django.contrib import messages
from .models import UserQuries, AdServerLead
from .tasks import create_lead_crm


# Register your models here.
def lead_creted_on_crm(modeladmin, request, queryset):
    for query in queryset:
        query_dict = {}
        try:
            # usr_query = UserQuries.objects.get(id=query.id)
            # query_dict.update({
            #     'name': usr_query.name,
            #     'email': usr_query.email,
            #     'country_code': usr_query.country.phone,
            #     'mobile': usr_query.phn_number,
            #     'message': usr_query.message,
            #     'source': usr_query.source,
            #     'lsource': usr_query.lead_source,
            #     'product': usr_query.product,
            #     'product_id': usr_query.product_id,
            #     'medium': usr_query.medium,
            #     'path': usr_query.path,
            #     'source':usr_query.source,
            #     'utm_parameter':usr_query.utm_parameter,
            #     'campaign_slug':usr_query.campaign_slug,
            # })
            # query_dict.update({
            #     'queryid': query.id})
            # post_psedu_lead.delay(query_dict)
            
            if not query.lead_created:
                create_lead_crm(pk=query.pk)
                # messages.add_message(
                # request, messages.SUCCESS, "lead created")
                # messages.add_message(
                # request, messages.ERROR, "lead already created")
                
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
lead_creted_on_crm.short_description = 'create lead on crm'


class UserQuriesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'phn_number', 'email', 'message',
        'product', 'lead_created', 'inactive',
        'lead_source', 'source', 'created', 'modified'
    )
    ordering = ['-created']
    actions = [lead_creted_on_crm]
    list_filter = ('lead_source', 'medium')
    search_fields = ('id', 'phn_number', 'email')
    list_per_page = 50


class AdServerLeadAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'country_code', 'mobile', 'source',
        'url', 'created',
        'inactive', 'added_on'
    )
    ordering = ['-added_on']
    list_per_page = 20


admin.site.register(UserQuries, UserQuriesAdmin)
admin.site.register(AdServerLead, AdServerLeadAdmin)
