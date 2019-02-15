import os, django, sys
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

if __name__ == '__main__':

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")

    ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
    ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

    if ROOT_FOLDER not in sys.path:
        sys.path.insert(1, ROOT_FOLDER + '/')

    #  setup django
    django.setup()

    # import inter apps
    from core.mixins import InvoiceGenerate

    obj = InvoiceGenerate()
    pdf_file = obj.generate_pdf({"STATIC_URL": settings.STATIC_URL, "SITE_DOMAIN": settings.SITE_DOMAIN,
                                 "SITE_PROTOCOL": settings.SITE_PROTOCOL}, 'emailers/candidate/resume_test.html')
    file_path = os.path.join(os.path.dirname(__file__))
    file_name = 'test.pdf'
    pdf_file = SimpleUploadedFile(
        file_name, pdf_file,
        content_type='application/pdf')
    dest = open(
        file_path + file_name, 'wb')
    for chunk in pdf_file.chunks():
        dest.write(chunk)
    dest.close()
