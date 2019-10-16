#python imports

#django imports

#local imports

#inter app imports

#third party imports
from rest_framework.pagination import PageNumberPagination

class LearningCustomPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100

	# def paginate_queryset(self, queryset, request, view=None):
	# 	import ipdb;ipdb.set_trace()
	# 	if 'nopage' in request.query_params:
	# 		return None
	# 	return super(LearningCustomPagination,self).paginate_queryset(
	# 		queryset,request,view)