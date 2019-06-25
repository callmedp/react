from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect

class ListPartialMixin(object):
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        context = {'page': serializer.data, 'page_object': self.paginator.page,
            'received_kwargs': kwargs, 'partial_template': self.partial_template_name, 'doing_partial': request.META.get('HTTP_X_PJAX')}
        if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
            context['is_vendee'] = True
            context['vendor_id'] = self.request.user.vendor_set.all()[0].id
        if request.user and request.user.is_staff:
            context['is_admin'] = True
        return Response(data=context, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)


class DetailPartialMixin(object):
    renderer_classes = [TemplateHTMLRenderer]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        context = {'serializer': serializer, 'received_kwargs': kwargs, 'instance': instance, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}
        if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
            context['is_vendee'] = True
            context['vendor_id'] = self.request.user.vendor_set.all()[0].id
        if request.user and request.user.is_staff:
            context['is_admin'] = True
        return Response(data=context, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)


class UpdatableDetailPartialMixin(DetailPartialMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            context = {'serializer': serializer, 'received_kwargs': kwargs, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}
            if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
                context['is_vendee'] = True
                context['vendor_id'] = self.request.user.vendor_set.all()[0].id
            if request.user and request.user.is_staff:
                context['is_admin'] = True
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if hasattr(self, 'success_list_redirect') and self.success_list_redirect:
            return redirect(self.success_list_redirect)
        elif hasattr(self, 'success_detail_redirect') and self.success_detail_redirect:
            return redirect(self.success_detail_redirect, pk=serializer.data.get('id'))
        else:
            context = {'serializer': 'serializer', 'received_kwargs': kwargs, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}
            if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
                context['is_vendee'] = True
                context['vendor_id'] = self.request.user.vendor_set.all()[0].id
            if request.user and request.user.is_staff:
                context['is_admin'] = True
            return Response(data=context, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name , status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AddPartialMixin(object):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        context = {'serializer': serializer, 'received_kwargs': kwargs, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}
        if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
            context['is_vendee'] = True
            context['vendor_id'] = self.request.user.vendor_set.all()[0].id
        if request.user and request.user.is_staff:
            context['is_admin'] = True
        return Response(data=context, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            context = {'serializer': serializer, 'received_kwargs': kwargs, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}
            if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
                context['is_vendee'] = True
                context['vendor_id'] = self.request.user.vendor_set.all()[0].id
            if request.user and request.user.is_staff:
                context['is_admin'] = True
            return Response(data=context, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if hasattr(self, 'success_list_redirect') and self.success_list_redirect:
            return redirect(self.success_list_redirect)
        elif hasattr(self, 'success_detail_redirect') and self.success_detail_redirect:
            return redirect(self.success_detail_redirect, pk=serializer.data.get('id'))
        else:
            context = {'serializer': 'serializer', 'received_kwargs': kwargs, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}
            if hasattr(self.request.user, 'vendor_set') and self.request.user.vendor_set.count():
                context['is_vendee'] = True
                context['vendor_id'] = self.request.user.vendor_set.all()[0].id
            if request.user and request.user.is_staff:
                context['is_admin'] = True
            return Response(data=context, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name , status=status.HTTP_201_CREATED, headers=headers)
