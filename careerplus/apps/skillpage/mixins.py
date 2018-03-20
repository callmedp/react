import json
import requests
import logging


class SkillPageMixin(object):

    def get_job_count_and_fuctionan_area(self, slug):
        data_dict = {}
        try:
            url = "https://www.shine.com/api/v2/search/simple/?q={}".format('"'+ slug + '"')
            response = requests.get(url)
            if response.status_code == 200:
                response_data = response.json()
                data_dict.update({
                    'job_count': response_data['count'],
                    'jFArea': response_data.get('facets', {}).get('fields').get('jFArea')
                })
                return data_dict
        
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return data_dict
