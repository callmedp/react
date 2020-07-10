#python imports
import logging
import rest_framework

from collections import OrderedDict

#django imports

from django.db.models import QuerySet
from django.core.exceptions import ImproperlyConfigured



#3rd party imports
from sorl.thumbnail import get_thumbnail



class SerializerFieldsMixin(object):
    """
    Return only the fields asked for.
    Don't return any extra fields in serializer.
    """
    def get_fields(self):
        all_fields = super(SerializerFieldsMixin, self).get_fields()
        asked_fields = self.context.get('asked_fields',"")
        if not asked_fields:
            return all_fields
        all_fields = OrderedDict([(k, v) for k, v in all_fields.items() if k in asked_fields])
        return all_fields


class FieldFilterMixin(object):
    """
    To be used with List/Retrieve views.
    Set class attribute fields for the fields you want to display.
    Or override get_required_fields to customize.
    """

    def get_required_fields(self):
        if self.request.GET.get("fl", None):
            return self.request.GET.get("fl").split(',')

        try:
            instance = self.get_object()
            return [field.name for field in instance._meta.fields if field]
        except:
            return []

    def get_serializer_context(self):
        methods_to_act_on = ["GET", "HEAD"]
        context = super(FieldFilterMixin, self).get_serializer_context()
        asked_fields = self.get_required_fields()
        if asked_fields and self.request.method in methods_to_act_on:
            context["asked_fields"] = asked_fields
        return context


class ListSerializerContextMixin(object):

    list_lookup_fields = ['user_id']
    fields_required_mapping = {'user_id': ['first_name', 'last_name', 'image', 'level','slug']}
    # field_model_mapping = {'user_id':User}

    multiple_parent_field_mapping = {}
    multiple_parent_model_mapping = {}
    multiple_parent_fields_required_mapping = {}

    def update_context(self, include_item_data, lookup_field, include_item_type=-1):
        if include_item_type == -1:
            context_key = lookup_field + '_ids'
        else:
            context_key = lookup_field + "_" + str(include_item_type) + "_ids"

        if not isinstance(include_item_data, list):
            include_item_data = [include_item_data]

        if not self.context.get(context_key):
            self.context[context_key] = include_item_data
        else:
            self.context[context_key] = self.context[context_key] + include_item_data

    def get_item_fields_required(self, item):
        if not hasattr(self, 'fields_required_mapping'):
            raise ImproperlyConfigured("'%s' must define fields_required_mapping" %self.__class__.__name__)

        fields_required = self.fields_required_mapping.get(item, [])

        if not fields_required:
            raise ImproperlyConfigured("'%s' must define required fields for %s" %(self.__class__.__name__,item))

        if not isinstance(fields_required, list):
            raise ImproperlyConfigured("Required fields for %s must be a list" %item)

        fields_required = list(set(fields_required + ['id']))
        return fields_required

    def get_field_model_class(self, item):
        if not hasattr(self, 'field_model_mapping'):
            raise ImproperlyConfigured("'%s' must define field_model_mapping" % self.__class__.__name__)

        if not isinstance(self.field_model_mapping, dict):
            raise ImproperlyConfigured("field_model_mapping fields for %s must be a dict" %item)

        model_class = self.field_model_mapping.get(item)

        if not model_class:
            raise ImproperlyConfigured("No model found for %s" % item)

        return model_class

    def to_representation(self, instance):
        ret = super(ListSerializerContextMixin, self).to_representation(instance)
        if not self.include_keys or not instance:
            return ret

        for lookup_field in self.include_keys:
            if '__' in lookup_field:
                embed = True
                embed_field = lookup_field.split('__')
                parent_field = embed_field[0]
                child_field = embed_field[1]
                embed_document = getattr(instance, parent_field)
                instance_field_data = getattr(embed_document, child_field)

            else:
                instance_field_data = getattr(instance, lookup_field)

            context_key_data = getattr(self, lookup_field + "_data", {})

            if not isinstance(instance_field_data, list):
                d = {}
                for key, value in context_key_data.get(str(instance_field_data), {}).items():
                    d[key] = value
                ret.update({"%s_data" % lookup_field: [d]})
                continue

            ret["%s_data" % lookup_field] = []

            for key in instance_field_data:
                d = {}
                for key, value in context_key_data.get(str(key), {}).items():
                    d[key] = value
                ret["%s_data" % lookup_field].append(d)

        return ret


class ListSerializerDataMixin(object):

    _requests_allowed = ['GET']

    def __init__(self, instance=None, data=None, **kwargs):
        """
        Override the __init__ to include user data inside API response.
        The request must carry the include_user parameter.
        """

        super(ListSerializerDataMixin, self).__init__(instance, data, **kwargs)

        if not 'request' in self.context.keys():
            return
        field_checkup_list = self.list_lookup_fields + list(self.multiple_parent_field_mapping.keys())
        self.include_keys = [key for key in field_checkup_list if 'include_' + key in self.context['request'].GET.keys()]
        self.single_parent_keys = [key for key in self.list_lookup_fields if 'include_'+key in self.context['request'].GET.keys()]
        self.multiple_parent_keys = [key for key in self.multiple_parent_field_mapping.keys() if 'include_'+key in self.context['request'].GET.keys()]
        if not self.include_keys or not instance:
            return
        if type(instance) is list or isinstance(instance, QuerySet):

            for obj in instance:
                for lookup_field in self.include_keys:
                    embed = False
                    if '__' in lookup_field:
                        embed = True
                        embed_field = lookup_field.split('__')
                        parent_field = embed_field[0]
                        child_field = embed_field[1]

                    if lookup_field in self.multiple_parent_field_mapping.keys():

                        self.update_context(
                            getattr(obj, lookup_field),
                            lookup_field,
                            getattr(obj, self.multiple_parent_field_mapping[lookup_field])
                        )
                    else:
                        if not embed:
                            field_value = getattr(obj, lookup_field)
                        else:
                            embed_document = getattr(obj, parent_field)
                            field_value = getattr(embed_document, child_field)
                        self.update_context(field_value, lookup_field)

        else:
            for lookup_field in self.include_keys:

                embed = False

                if '__' in lookup_field:
                    embed = True
                    embed_field = lookup_field.split('__')
                    parent_field = embed_field[0]
                    child_field = embed_field[1]

                if lookup_field in self.multiple_parent_field_mapping.keys():
                    self.update_context(
                        getattr(instance, lookup_field),
                        lookup_field,
                        getattr(instance, self.multiple_parent_field_mapping[lookup_field])
                    )
                else:
                    if not embed:
                        field_value = getattr(instance, lookup_field)
                    else:
                        embed_document = getattr(instance, parent_field)
                        field_value = getattr(embed_document, child_field)

                    self.update_context(field_value, lookup_field)

        for key in self.single_parent_keys:
            setattr(self, key + '_data', self.update_single_parent_item_data(key))

        for key in self.multiple_parent_keys:
            setattr(self, key + '_data', self.update_multiple_parent_item_data(key))

    def _get_method_fields_data(self, get_param, obj):
        method_data = {}
        param_method_fields_mapping = getattr(self, "param_method_fields_mapping",{})
        param_method_name_mapping = getattr(self, "param_method_name_mapping",{})

        for get_field, obj_fields in param_method_fields_mapping.items():
            if not self.context['request'].GET.has_key(get_field):
                continue
            get_field_value = self.context['request'].GET.get(get_field)
            for field in obj_fields:
                object_method_to_invoke = param_method_name_mapping.get(field,"")
                method_data.update({field: getattr(obj, object_method_to_invoke)(get_field_value)})

        return method_data

    def update_single_parent_item_data(self, item):
        """
        Update all the users required inside instance data.
        Also, check the fields to be used.
        """
        field_name = item
        item_id_mapping = {}
        item_id_list = self.context[item + '_ids']
        item_fields_required = self.get_item_fields_required(item)
        model_class = self.get_field_model_class(item)
        items = model_class.objects.filter(id__in=item_id_list)

        for item in items:
            if str(item.id) in item_id_mapping.keys():
                continue
            data = OrderedDict('').copy()
            data['id'] = str(item.id)
            for field in item_fields_required:
                if field == 'id':
                    continue
                data.update({field: getattr(item, field)})

            get_params = getattr(self, "field_param_mapping", {}).get(field_name,[])
            for get_param in get_params:
                data.update(self._get_method_fields_data(get_param, item))

            item_id_mapping.update({str(item.id): data})
        return item_id_mapping

    def update_multiple_parent_item_data(self, item):
        item_id_mapping = {}
        item_type_key = self.multiple_parent_field_mapping[item]
        valid_types = self.multiple_parent_model_mapping[item_type_key].keys()

        for item_type in valid_types:
            item_id_list = self.context.get(item + '_' + str(item_type) + '_ids')
            if not item_id_list:
                continue
            item_id_list = [x for x in item_id_list if ObjectId.is_valid(x) or isinstance(x,int)]
            item_fields_required = self.multiple_parent_fields_required_mapping[item_type_key][item_type]
            model_class = self.multiple_parent_model_mapping[item_type_key][item_type]
            items = model_class.objects.filter(id__in=item_id_list)

            for parent_item in items:
                if str(parent_item.id) in item_id_mapping.keys():
                    continue
                data = OrderedDict('').copy()
                data['id'] = str(parent_item.id)
                for field in item_fields_required:
                    if field == 'id':
                        continue
                    data.update({field: getattr(parent_item, field)})

                get_params = getattr(self, "field_param_mapping", {}).get(item,[])
                for get_param in get_params:
                    data.update(self._get_method_fields_data(get_param, parent_item))

                item_id_mapping.update({str(parent_item.id): data})

        return item_id_mapping


class ImageThumbnailMixin(object):

    def to_representation(self, instance):
        ret = super(ImageThumbnailMixin, self).to_representation(instance)

        image_fields = [im for im in self.fields if type(self.fields.get(im)) ==
                        rest_framework.fields.ImageField]
        if not image_fields:
            return ret

        request = self.context.get('request')

        images_to_be_processed = [field for field in image_fields if
                                  request.query_params.get(field + '_size')]
        if not images_to_be_processed:
            return ret

        for img in images_to_be_processed:
            if not ret.get(img):
                continue
            for size in request.query_params.get(img + '_size').split(','):
                try:
                    ret.update({img + '_' + str(size): get_thumbnail(ret.get(
                                    img),size,quality=70).url})
                except Exception as e:
                    logging.getLogger('error_log').error("error in "
                    "get_thumbnail for {}".format(img, str(e)))
        return ret




