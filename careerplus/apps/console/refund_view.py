from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django.contrib import messages


from order.models import RefundRequest, Order
from blog.mixins import PaginationMixin
from core.mixins import InvoiceGenerate
from order.choices import TYPE_REFUND


class RefundOrderRequestView(ListView, PaginationMixin):
    context_object_name = 'refund_request_list'
    template_name = 'console/refund/refund-request-list.html'
    model = RefundRequest
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(RefundOrderRequestView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(
            RefundOrderRequestView, self).get_context_data(**kwargs)
        paginator = Paginator(
            context['refund_request_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "messages": alert,
            "query": self.query,
        })
        return context

    def get_queryset(self):
        queryset = super(RefundOrderRequestView, self).get_queryset()
        return queryset


class RefundRaiseRequestView(TemplateView):
    template_name = 'console/refund/raise-refundrequest.html'
    model = Order
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.query = ''

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get('query', '')
        return super(RefundRaiseRequestView, self).get(request, args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super(
            RefundRaiseRequestView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        order = None
        if self.query:
            try:
                order = Order.objects.get(number=self.query, status=1)
            except Exception as e:
                messages.add_message(self.request, messages.ERROR, str(e))
        context.update({
            "messages": alert,
            "query": self.query,
        })
        if order:
            orderitems = InvoiceGenerate().get_order_item_list(order=order)
            context.update({
                "order": order,
                "orderitems": orderitems,
            })

        context.update({
            "type_refund_dict": dict(TYPE_REFUND),
        })

        return context