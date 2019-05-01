from django.contrib import admin
from . import models
from order.choices import BOOSTER_RECRUITER_TYPE
from django import forms
import csv
import re

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
    list_display = ('id', 'name', 'skill', "vendor_provider", "vendor_text")
    model = models.Certificate


class UserCertificateAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'year', 'candidate_email',
        'candidate_mobile', 'certificate', "get_vendor")
    model = models.UserCertificate

    def get_vendor(self, obj):
        return obj.certificate.vendor_provider
    get_vendor.short_description = 'Vendor'


class BoosterRecruiterAdminForm(forms.ModelForm):
    model = models.BoosterRecruiter

    def clean(self):
        recruiter_type = self.cleaned_data['type_recruiter']
        if not self.instance.id:
            recruiter_type = models.BoosterRecruiter.objects.filter(type_recruiter=recruiter_type)
            if recruiter_type.exists():
                raise forms.ValidationError("This Recruiter type already exists")

        else:
            recruiter_type = models.BoosterRecruiter.objects.filter(
                type_recruiter=recruiter_type
            ).exclude(id=self.instance.id)
            if recruiter_type.exists():
                raise forms.ValidationError("This Recruiter type already exists")

        return self.cleaned_data


class BoosterRecruiterAdmin(admin.ModelAdmin):
    list_display = (
        'type_recruiter',
    )
    form = BoosterRecruiterAdminForm

    def changelist_view(self, request, extra_context=None):        

        if request.method == 'POST' and 'upload_booster_recruiter' == request.POST.get('action', None):
            from django.contrib import messages
            try:
                file = request.FILES.get('upload_file', None)
                recruiter_type = request.POST.get('recruiter_type', None)
                recruiters = []
                email_added = []
                email_presents = []
                if file and recruiter_type:
                    boosterrecruiter, created = models.BoosterRecruiter.objects.get_or_create(type_recruiter=recruiter_type)
                    recruiter_type = int(recruiter_type)
                    file_data = file.read().decode("utf-8")
                    uploaded_file = csv.reader(file_data.splitlines())
                    if boosterrecruiter.recruiter_list:
                        email_presents = [re.findall(r"<.*>", email)[0].replace('<','').replace('>','') for email in boosterrecruiter.recruiter_list.split(',')]
                    for index, line in enumerate(uploaded_file):
                        if index == 0:
                            continue
                        name, email = line
                        name = name.strip()
                        email = email.strip()

                        if email not in email_added and email not in email_presents and email:
                            recruiters.append(name + '<' + email + '>')
                            email_added.append(email)
                        else:
                            continue
                    recruiter_name_email_as_string = ",".join(recruiters)
                    if boosterrecruiter.recruiter_list and recruiters:
                        boosterrecruiter.recruiter_list += ','

                    boosterrecruiter.recruiter_list += recruiter_name_email_as_string
                    boosterrecruiter.save()
                else:
                    # Then, when you need to error the user:
                    messages.error(request, "Recruiter Type or File is not Provided")
            except Exception as e:
                messages.error(request, str(e))
        extra_context = extra_context or {}
        extra_context['booster_recruiter_type'] = BOOSTER_RECRUITER_TYPE
        return super(BoosterRecruiterAdmin, self).changelist_view(request, extra_context=extra_context)


class AssesmentAdmin(admin.ModelAdmin):
    list_display = ('candidate_email', "assesment_name", "report")
    model = models.Assesment


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('assesment', 'subject', "score_obtained")
    model = models.Score

class UserCertificateOperationsAdmin(admin.ModelAdmin):
    model = models.UserCertificateOperations


admin.site.register(models.Vendor, VendorAdmin)
admin.site.register(models.Certificate, CeritficateAdmin)
admin.site.register(models.UserCertificate, UserCertificateAdmin)
admin.site.register(models.BoosterRecruiter, BoosterRecruiterAdmin)
admin.site.register(models.Assesment, AssesmentAdmin)
admin.site.register(models.Score, ScoreAdmin)
admin.site.register(models.UserCertificateOperations, UserCertificateOperationsAdmin)


