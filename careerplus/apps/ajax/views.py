import json
import logging
import datetime

from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from cms.models import Page
from cms.mixins import LoadMoreMixin
from shop.models import Category
from blog.models import Blog, Comment


class ArticleCommentView(View):
	def post(self, request, *args, **kwargs):
		status = 0
		if request.is_ajax():
			try:
				message = request.POST.get('message').strip()
				slug = request.POST.get('slug').strip()
				blog = Blog.objects.get(slug=slug)
				if request.session.get('candidate_id') and message:
					Comment.objects.create(blog=blog, message=message, candidate_id=request.session.get('candidate_id'))
					status = 1
					blog.no_comment += 1
					blog.save()
			except Exception as e:
				logging.getLogger('error_log').error("%s " % str(e))
				pass
			data = {"status": status}
			return HttpResponse(json.dumps(data), content_type="application/json")
		else:
			return HttpResponseForbidden


class ArticleShareView(View):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			article_slug = request.GET.get('article_slug')
			try:
				obj = Blog.objects.get(slug=article_slug)
				obj.no_shares += 1
				obj.update_score()
				obj.save()
			except:
				pass
			data = {"status": "success"}
			return HttpResponse(json.dumps(data), content_type="application/json")


class AjaxCommentLoadMoreView(View, LoadMoreMixin):

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			slug = request.POST.get('slug', '')
			page = int(request.POST.get('page', 1))
			try:
				page_obj = Page.objects.get(slug=slug, is_active=True)
				comments = page_obj.comment_set.filter(is_published=True,
					is_removed=False)
				comment_list = self.pagination_method(page=page,
					comment_list=comments, page_obj=page_obj)
				return HttpResponse(json.dumps({'comment_list': comment_list}))
			except Exception as e:
				logging.getLogger('error_log').error("%s " % str(e))


class CmsShareView(View):
	
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			page_id = request.GET.get('page_id')
			try:
				obj = Page.objects.get(id=page_id)
				obj.total_share += 1
				obj.save()
				today = timezone.now()
				today_date = datetime.date(day=1, month=today.month, year=today.year)
				pg_counter, created = self.page_obj.pagecounter_set.get_or_create(count_period=today_date)
				pg_counter.no_shares += 1
				pg_counter.save()

			except:
				pass
			data = ["Success"]
			return HttpResponse(json.dumps(list(data)), content_type="application/json")



class AjaxProductLoadMoreView(TemplateView):
    template_name = 'include/load_product.html'

    def get(self, request, *args, **kwargs):
        return super(AjaxProductLoadMoreView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AjaxProductLoadMoreView, self).get_context_data(**kwargs)
        slug = self.request.GET.get('slug', '')
        page = int(self.request.GET.get('page', 1))
        try:
            page_obj = Category.objects.get(slug=slug, active=True)
            products = page_obj.product_set.all()
            paginator = Paginator(products, 2)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = 0
            context.update({'products': products, 'page': page, 'slug': slug})
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
        return context
