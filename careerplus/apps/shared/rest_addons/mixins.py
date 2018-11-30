from collections import OrderedDict


class SerializerFieldsMixin(object):
    """
    Return only the fields asked for.
    Don't return any extra fields in serializer.
    """
    def get_fields(self):
        all_fields = super(SerializerFieldsMixin, self).get_fields()
        asked_fields = self.context.get('asked_fields')
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
            return self.request.GET.get("fl")
        try:
            return self.fields
        except:
            return []

    def get_serializer_context(self):
        methods_to_act_on = ["GET", "HEAD"]
        context = super(FieldFilterMixin, self).get_serializer_context()
        asked_fields = self.get_required_fields()
        if asked_fields and self.request.method in methods_to_act_on:
            context["asked_fields"] = asked_fields
        return context
