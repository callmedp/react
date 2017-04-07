import os
import csv
import logging

from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class UploadInFile(object):

	def write_in_file(self, data_dict={}):
		try:
			name = data_dict.get('name', '').strip()
			mobile = data_dict.get('mobile', '').strip()
			email = data_dict.get('email', '').strip()
			path = data_dict.get('path', '').strip()
			message = data_dict.get('message', '')
			today = timezone.now()
			filename = today.strftime("%Y-%d-%m") + '_lead.csv'
			file_dir = settings.LEAD_UPLOAD
			file_path = file_dir + filename
			if os.path.exists(file_path):
				with open(file_path, 'a') as csvfile:
					fieldnames = ['name', 'mobile', 'email', 'message', 'path']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writerow({
						"name": name,
						"mobile": mobile,
						"email": email,
						"message": message,
						"path": path
					})
			else:
				with open(file_path, 'w') as csvfile:
					fieldnames = ['name', 'mobile', 'email', 'message', 'path']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
					writer.writeheader()
					writer.writerow({
						"name": name,
						"mobile": mobile,
						"email": email,
						"message": message,
						"path": path
					})
		except Exception as e:
			logging.getLogger('error_log').error(str(e))


class LoadMoreMixin(object):
	def pagination_method(self, page, comment_list, page_obj):
		paginator = Paginator(comment_list, 1)
		try:
			comments = paginator.page(page)
		except PageNotAnInteger:
			comments = paginator.page(1)
		except EmptyPage:
			comments = paginator.page(paginator.num_pages)  # If page is out of range (e.g. 9999), deliver last page of results.
		return render_to_string('include/load_comment.html', {'comments': comments, "page_obj": page_obj})