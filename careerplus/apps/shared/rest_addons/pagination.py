#python imports

#django imports

#local imports

#inter app imports

#third party imports
from rest_framework.pagination import PageNumberPagination

class LearningCustomPagination(PageNumberPagination):
	page_size = 2
	page_size_query_param = 'page_size'
	max_page_size = 100