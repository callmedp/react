#python imports

#django imports

#local imports

#inter app imports

#third party imports
from rest_framework.pagination import PageNumberPagination

class Learning_custom_pagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100