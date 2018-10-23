import os
import csv
import logging

from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class UploadInFile(object):

    def write_in_file(self, data_dict={}):
        try:
            name = data_dict.get('name', '').strip()
            country_code = data_dict.get('country', '91')
            mobile = data_dict.get('phn_number', '').strip()
            email = data_dict.get('email', '').strip()
            path = data_dict.get('path', '').strip()
            message = data_dict.get('message', '')
            today = timezone.now()
            filename = today.strftime("%Y-%m-%d") + '_lead.csv'
            file_dir = settings.LEAD_UPLOAD
            file_path = file_dir + filename
            if os.path.exists(file_path):
                with open(file_path, 'a') as csvfile:
                    fieldnames = ['name', 'country_code', 'mobile', 'email', 'message', 'path']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({
                        "name": name,
                        "country_code": country_code,
                        "mobile": mobile,
                        "email": email,
                        "message": message,
                        "path": path
                    })
            else:
                with open(file_path, 'w') as csvfile:
                    fieldnames = ['name', 'country_code', 'mobile', 'email', 'message', 'path']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        "name": name,
                        "country_code": country_code,
                        "mobile": mobile,
                        "email": email,
                        "message": message,
                        "path": path
                    })
        except Exception as e:
            logging.getLogger('error_log').error(str(e))


class LoadMoreMixin(object):
    def pagination_method(self, page, comment_list, page_obj,page_size=2):
        paginator = Paginator(comment_list, page_size)
        csrf_token = get_token(self.request)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)  # If page is out of range (e.g. 9999),
                                                            # deliver last page of results.
        
        return render_to_string('include/load_comment.html',
                                {'comments': comments, "page_obj": page_obj, \
                                "csrf_token": csrf_token,"request":self.request})
