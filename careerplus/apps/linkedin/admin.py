from django.contrib import admin
from linkedin.models import Organization, Draft, Education


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
    inlines = [OrganizationInline, EducationInline]

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
        except:
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
        except:
            return '<b>No user</b>'
    candidate_info.short_descriptixon = 'Candidate Information'
    candidate_info.allow_tags = True

admin.site.register(Draft, DraftAdmin)