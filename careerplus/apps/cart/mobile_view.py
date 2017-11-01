import json

from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden

from .mixins import CartMixin
from .models import Cart


class RemoveFromCartMobileView(View, CartMixin):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {"status": -1}
            product_reference = request.POST.get('product_reference')
            child_list = request.POST.getlist('child_list', [])
            try:
                if not self.request.session.get('cart_pk'):
                    self.getCartObject()

                cart_pk = self.request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    if child_list:
                        for child_ref in child_list:
                            line_obj = cart_obj.lineitems.get(reference=child_ref)
                            if line_obj.parent_deleted:
                                parent = line_obj.parent
                                childs = cart_obj.lineitems.filter(
                                    parent=parent, parent_deleted=True)
                                if childs.count() > 1:
                                    line_obj.delete()
                                else:
                                    parent.delete()
                            else:
                                line_obj.delete()
                    elif product_reference:
                        line_obj = cart_obj.lineitems.get(
                            reference=product_reference)
                        if line_obj.parent_deleted:
                            parent = line_obj.parent
                            childs = cart_obj.lineitems.filter(
                                parent=parent, parent_deleted=True)
                            if childs.count() > 1:
                                line_obj.delete()
                            else:
                                parent.delete()
                        else:
                            line_obj.delete()
                    data['status'] = 1
                else:
                    data['error_message'] = 'this cart item alredy removed.'

            except Exception as e:
                data['error_message'] = str(e)

            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()