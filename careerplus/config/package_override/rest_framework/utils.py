# python imports

# django imports

# local imports

# inter app imports

# third party imports
from rest_framework import serializers


@property
def paginator(self):
	"""
	The paginator instance associated with the view, or `None`.
	"""
	if self.request.GET.get('nopage'):
		self._paginator = None
		return self._paginator

	if not hasattr(self, '_paginator'):
		if self.pagination_class is None:
			self._paginator = None
		else:
			self._paginator = self.pagination_class()
	return self._paginator

