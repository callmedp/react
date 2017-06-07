from django.template.defaultfilters import slugify


class SaveSlug(object):

    def save_slug(self, slug, name):
        try:
            if slug and '_' in slug:
                return slugify(slug.replace("_", "-"))
            elif not slug and name:
                return slugify(name.replace("_", "-"))
        except:
            pass
        return slug
