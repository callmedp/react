from django.contrib import admin
from linkedin.models import Organization, Draft, Education
from order.models import OrderItem
from django.utils import timezone
import logging


# Register your models here.
class OrganizationInline(admin.TabularInline):
    model = Organization
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class DraftAdmin(admin.ModelAdmin):
    model = Draft
    list_display = ['pk', 'get_order', 'candidate_info']
    search_fields = ('id',)
    inlines = [OrganizationInline, EducationInline]

    # def save_model(self, request, obj, form, change):
    #     try:
    #         ord_obj = OrderItem.objects.get(oio_linkedin=obj)
    #         last_status = ord_obj.oi_status
    #         ord_obj.oi_status = 45  # pending Approval
    #         ord_obj.last_oi_status = last_status
    #         ord_obj.draft_added_on = timezone.now()
    #         ord_obj.save()
    #         ord_obj.orderitemoperation_set.create(
    #             linkedin=obj,
    #             draft_counter=ord_obj.draft_counter + 1,
    #             oi_status=44,
    #             last_oi_status=last_status,
    #             assigned_to=ord_obj.assigned_to,
    #             added_by=request.user)
    #         ord_obj.orderitemoperation_set.create(
    #             oi_status=ord_obj.oi_status,
    #             last_oi_status=44,
    #             assigned_to=ord_obj.assigned_to,
    #             added_by=request.user)
    #     except:
    #         pass

    def queryset(self, request):
        qs = super(DraftAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            qs = qs.filter(
                orderitem__order__status=1, no_process=False,
                orderitem__product__type_flow=8,
                orderitem__assigned_to=request.user)
            return qs

    def get_order(self, obj):
        try:
            return obj.orderitem.order_id
        except Exception as e:
            logging.getLogger('error_log').error('unable to return order item object id %s' % str(e))
            return ''
    get_order.short_description = 'Order ID'

    def candidate_info(self, obj):
        try:
            order = obj.orderitem.order
            if order.candidate_id:
                return '<b>Email:</b> %s <br/><b>Mobile:</b>%s %s <br><b>Name:</b> %s %s' % (
                    order.email, order.country_code, order.mobile,
                    order.first_name, order.last_name)
            else:
                return '<b>No user</b>'
        except Exception as e:
            logging.getLogger('error_log').error('unable to get candidate information %s'%str(e))
            return '<b>No user</b>'
    candidate_info.short_descriptixon = 'Candidate Information'
    candidate_info.allow_tags = True

admin.site.register(Draft, DraftAdmin)