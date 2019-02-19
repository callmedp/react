from django.contrib import admin
from . import models
from order.choices import BOOSTER_RECRUITER_TYPE

class VendorHierarchyInline(admin.TabularInline):
    model = models.VendorHierarchy
    extra = 1


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'email', 'mobile', 'pan', 'website')
    inlines = [VendorHierarchyInline]
    model = models.VendorHierarchy
    fk_name = 'vendee'
    readonly_fields = ('modified',)
    raw_id_fields = ('city', 'country','state')
    extra = 0


class CeritficateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'skill', "vendor_provider")
    model = models.Certificate


class UserCertificateAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'year', 'candidate_email',
        'candidate_mobile', 'certificate', "get_vendor")
    model = models.UserCertificate

    def get_vendor(self, obj):
        return obj.certificate.vendor_provider
    get_vendor.short_description = 'Vendor'


class BoosterRecruiterAdmin(admin.ModelAdmin):
    list_display = (
        'type_recruiter',
    )

    def changelist_view(self, request, extra_context=None):        

        if request.method == 'POST' and 'upload_booster_recruiter' == request.POST.get('action', None):
            from django.contrib import messages
            try:
                file = request.FILES.get('upload_file', None)
                recruiter_type = request.POST.get('recruiter_type', None)
                recruiters = []
                email_added = []
                if file and recruiter_type:
                    recruiter_type = int(recruiter_type)
                    file_data = file.read().decode("utf-8")
                    lines = file_data.split("\n")
                    for index, line in enumerate(lines):
                        if index == 0:
                            continue
                        name, email = line.split(',')
                        name = name.strip()
                        email = email.strip()
                        if email not in email_added:
                            recruiters.append(name + '<' + email + '>')
                            email_added.append(email)
                        else:
                            continue
                        recruiter_name_email_as_string = ",".join(recruiters)
                        boosterrecruiter, created = models.BoosterRecruiter.objects.get_or_create(type_recruiter=recruiter_type)
                        boosterrecruiter.recruiter_list = recruiter_name_email_as_string
                        boosterrecruiter.save()
                else:
                    # Then, when you need to error the user:
                    messages.error(request, "Recruiter Type or File is not Provided")
            except Exception as e:
                messages.error(request, str(e))
        extra_context = extra_context or {}
        extra_context['booster_recruiter_type'] = BOOSTER_RECRUITER_TYPE
        return super(BoosterRecruiterAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.Certificate, CeritficateAdmin)
admin.site.register(models.UserCertificate, UserCertificateAdmin)
admin.site.register(models.BoosterRecruiter, BoosterRecruiterAdmin)
