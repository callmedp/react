from django.views.generic import View, TemplateView
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import Http404
from django.middleware.csrf import get_token

from .models import Page, Comment


class CMSPageView(TemplateView):
    model = Page
    template_name = "cms/cms_page.html"
    page_obj = None

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        try:
            self.page_obj = Page.objects.get(slug=slug)
        except Exception:
            raise Http404
        context = super(CMSPageView, self).get(request, *args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message', '')
        slug = kwargs.get('slug', None)
        try:
            self.page_obj = Page.objects.get(slug=slug)
        except Exception:
            raise Http404
        if request.user.is_authenticated() and message and self.page_obj:
            Comment.objects.create(created_by=request.user, message=message, page=self.page_obj)
        return HttpResponseRedirect(
            reverse('cms:page', kwargs={'slug': slug}))

    def get_context_data(self, **kwargs):
        context = super(CMSPageView, self).get_context_data(**kwargs)
        page_obj = self.page_obj
        left_widgets = page_obj.pagewidget_set.filter(section='left').select_related('widget')
        right_widgets = page_obj.pagewidget_set.filter(section='right').select_related('widget')
        context['left_widgets'] = ''
        context['right_widgets'] = ''
        context['page_obj'] = page_obj
        context['page_heading'] = page_obj.title
        download_docs = page_obj.document_set.filter(is_active=True)
        csrf_token_value = get_token(self.request)
        if download_docs.exists():
            download_doc = download_docs[0]
            context.update({
                'download_doc': download_doc
            })
        for left in left_widgets:
            widget_context = {}
            widget_context.update({
                'page_obj': page_obj,
                'widget': left.widget,
                'download_doc': download_doc,
                'csrf_token_value': csrf_token_value
            })
            widget_context.update(left.widget.get_widget_data())
            if left.widget.template_name:
                context['left_widgets'] += render_to_string('include/' + left.widget.template_name, widget_context)

        for right in right_widgets:
            widget_context = {}
            widget_context.update({
                'page_obj': page_obj,
                'widget': left.widget,
                'download_doc': download_doc,
                'csrf_token_value': csrf_token_value
            })
            widget_context.update(right.widget.get_widget_data())
            if right.widget.template_name:
                context['right_widgets'] += render_to_string('include/' + right.widget.template_name, widget_context)

        comments = page_obj.comment_set.filter(is_published=True, is_removed=False)
        context['comments'] = list(comments)
        context.update({'user': self.request.user})
        # if self.request.user.is_authenticated():
        #   comment_mod = page_obj.comment_set.filter(created_by=self.request.user,
        #       is_published=False, is_removed=False)

        #   if comment_mod.exists():
        #       under_mod = True
        #   else:
        #       under_mod = False

        #   context.update({'under_mod': under_mod})

        return context


class LoginToCommentView(View):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        page_obj = None
        try:
            page_obj = Page.objects.get(slug=slug)
        except Exception:
            raise Http404
        user_email = request.POST.get('user_email', None)
        user_password = request.POST.get('user_password', None)
        remember_me = request.POST.get('remember_me')
        user = authenticate(username=user_email, password=user_password)
        if user is not None:
            login(request, user)

        return HttpResponseRedirect(
            reverse('cms:page', kwargs={'slug': page_obj.slug}))


class LeadManagementView(View):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        data_dict = {}
        print (request.POST)
        pass


class DownloadPdfView(View):
    http_method_names = [u'post', ]
    
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        page_obj = None
        try:
            page_obj = Page.objects.get(slug=slug)
        except Exception:
            raise Http404

        try:
            pdf_obj = page_obj.document_set.filter(is_active=True)[0]
        except:
            pdf_obj = None

        if pdf_obj and pdf_obj.doc:
            extn = pdf_obj.doc.name.split('.')[-1]
            filename = slug + '.' + extn
            response = HttpResponse(pdf_obj.doc, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response