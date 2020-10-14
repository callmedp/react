from django.template import TemplateDoesNotExist



def get_contents(self, origin):
	try:
		with open(origin.name, encoding=self.engine.file_charset) as fp:
			return fp.read()
	except FileNotFoundError:
		raise TemplateDoesNotExist(origin)


def get_template_sources(self, template_name, template_dirs=None):
	template_name = self.prepare_template_name(template_name)
	for loader in self.template_source_loaders:
		if hasattr(loader, 'get_template_sources'):
			try:
				for result in loader.get_template_sources(template_name):
					yield result
			except UnicodeDecodeError:
				# The template dir name was a bytestring that wasn't valid
				# UTF-8.
				raise
			except ValueError:
				# The joined path was located outside of this particular
				# template_dir (it might be inside another one, so this isn't
				# fatal).
				pass

