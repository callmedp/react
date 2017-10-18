import logging

from order.models import Order, OrderItem
from core.api_mixin import UploadResumeToShine
from users.tasks import user_register


# @task(name="sync resume on shine")
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
			files = {
				'resume_file': oi.oi_draft,
			}

			flag = UploadResumeToShine().sync_candidate_resume_to_shine(
				candidate_id=order.candidate_id, files=files, data=data)
			print (flag)

	except Exception as e:
		logging.getLogger('task_log').error(
			"%s error in upload_resume_to_shine task" % (str(e)))
		print (str(e))