from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from shop.models import Product, PracticeTestInfo
from shared.rest_addons.mixins import SerializerFieldsMixin
from django.core.cache import cache
class ProductListSerializerForAuditHistory(SerializerFieldsMixin, ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')


class PracticeTestInfoCreateSerializer(ModelSerializer):
    has_completed = serializers.SerializerMethodField()

    class Meta:
        model = PracticeTestInfo
        fields = ('email', 'mobile_no', 'name', 'has_completed')

    def create(self, validated_data):
        try:
            test_info = PracticeTestInfo.objects.get(email=validated_data.get('email', None))
            test_info.save()
            # For non authenticated user, save email as per session key
            # for later use in payment login screen.
            if getattr(test_info, 'test_data', None):
                data = eval(getattr(test_info, 'test_data'))
                session = self.context['request'].session
                session_id = session.session_key
                if data['status'] == 'done' and 'candidate_id' not in session_id:    
                    cache.set('{}_neo_email_done'.format(session_id), test_info.email, 3600 * 24 * 30)
                    print(cache.get('{}_neo_email_done'.format(session_id)))
            return test_info
        except:
            return super(PracticeTestInfoCreateSerializer, self).create(validated_data)

    def get_has_completed(self, obj):
        return obj.has_completed
