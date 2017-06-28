from rest_framework import serializers
from geolocation import models

class LimitedSerializerMixin(serializers.ModelSerializer):
    class Meta:
        limit_fields = False
        limited_case_field = 'id'

    def __init__(self, *args, **kwargs):
        self.Meta.limit_fields = kwargs.pop('limit_fields', None)
        super(LimitedSerializerMixin, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        data = super(LimitedSerializerMixin, self).to_representation(obj)
        if self.Meta.limit_fields:
            return data.get(self.Meta.limited_case_field, None)
        return data

class CurrencySerializer(LimitedSerializerMixin):
    """
        Serializer for `Currency` model
    """
    class Meta:
        model = models.Currency
        fields = ('id', 'name', 'value', 'exchange_rate', 'offset')
        read_only_fields = ('id', 'name', 'value', 'exchange_rate', 'offset')
        limited_case_field = 'exchange_rate'

class CitySerializer(LimitedSerializerMixin):
    """
        Serializer for `City` model
    """
    class Meta:
        model = models.City
        fields = ('id', 'code_city', 'timezone', 'name', 'country')
        read_only_fields = ('id', 'code_city', 'timezone', 'name', 'country')
        limited_case_field = 'name'