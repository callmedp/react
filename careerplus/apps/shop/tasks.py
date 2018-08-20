
from shop.models import ProductAuditHistory
from celery.decorators import task


@task(name="add_log_in_product_audit_history")
def add_log_in_product_audit_history(**data):
    ProductAuditHistory.objects.create(**data)
