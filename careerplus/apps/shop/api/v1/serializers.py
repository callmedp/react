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

    def update_session_if_already_done_with_test(self, test_info):
        data = eval(getattr(test_info, 'test_data'))
        session = self.context['request'].session
        session_id = session.session_key
        if data['status'] == 'done' and 'candidate_id' not in session:
            cache.set('{}_neo_email_done'.format(session_id), test_info.email, 3600 * 24 * 30)
            print(cache.get('{}_neo_email_done'.format(session_id)))



    def create(self, validated_data):
        test_info = PracticeTestInfo.objects.filter(
            email=validated_data.get('email', None), order_item=None
        ).first()
        # For non authenticated user, save email as per session key
        # for later use in payment login screen.
        if test_info:
            return test_info
        else:
            return super(PracticeTestInfoCreateSerializer, self).create(validated_data)

    def get_has_completed(self, obj):
        email = obj.email
        test_infos = PracticeTestInfo.objects.filter(email=email)
        for info in test_infos:
            if info.has_completed:
                self.update_session_if_already_done_with_test(info)
                return True
        return False
