import logging

from django.conf import settings
from celery.decorators import task
from order.models import Order, OrderItem
from core.library.gcloud.custom_cloud_storage import GCPPrivateMediaStorage
from core.api_mixin import UploadResumeToShine
from users.tasks import user_register


@task(name="sync resume on shine")
def upload_resume_to_shine(oi_pk=None):
	try:
		oi = OrderItem.objects.get(pk=oi_pk)
		if not oi.order.candidate_id:
			user_register(data={}, order=oi.order.pk)
		order = Order.objects.get(pk=oi.order.pk)
		if oi.oi_draft and order.candidate_id:
			data = {
				'candidate_id': order.candidate_id,
				'upload_medium': 'direct',
				'upload_source': 'resume_builder',
			}
			file_path = settings.RESUME_DIR + oi.oi_draft.name
			if not settings.IS_GCP:
				resume_file = open(file_path, 'rb')
			else:
				resume_file = GCPPrivateMediaStorage().open(file_path)

			files = {
				'resume_file': resume_file,
			}

			flag = UploadResumeToShine().sync_candidate_resume_to_shine(
				candidate_id=order.candidate_id, files=files, data=data)
			if flag:
				logging.getLogger('info_log').info(
					"resume uploaded to shine for candidate -id : %s" % (str(order.candidate_id)))

	except Exception as e:
		logging.getLogger('error_log').error(
			"%s error in upload_resume_to_shine" % (str(e)))
