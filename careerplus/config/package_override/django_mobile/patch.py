

from django_mobile.loader import Loader

from .utils import get_contents,get_template_sources


def get_content():
	Loader.get_contents = get_contents

def get_template_source():
	Loader.get_template_sources = get_template_sources

