# Thirdparty apps imports
from filebrowser.base import FileObject


class ImageCompressedMixin(object):

    def save_image(self, image, variant=None):
        try:
            image_orig = FileObject(image.path)
            if image_orig.filetype == "Image":
                variant_list = [variant]
                if not variant:
                    variant_list = ['large', 'medium']
                for variant in variant_list:
                    image_orig.version_generate(variant)
                return True
        except:
            pass
        return False