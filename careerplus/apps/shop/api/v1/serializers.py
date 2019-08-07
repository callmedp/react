from rest_framework.serializers import ModelSerializer, ValidationError
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
    cefr_level = serializers.SerializerMethodField()
    class Meta:
        model = PracticeTestInfo
        fields = ('email', 'mobile_no', 'name', 'has_completed', 'cefr_level')

    def update_session_if_already_done_with_test(self, test_info):
        data = eval(getattr(test_info, 'test_data'))
        session = self.context['request'].session
        session_id = session.session_key
        if data['status'] == 'done' and 'candidate_id' not in session:
            cache.set('{}_neo_email_done'.format(session_id), test_info.email, 3600 * 24 * 30)

    def clean_email(self, email ):
        if not email[0].isalnum():
            raise ValidationError(
                'Email cannot start without an alphanumeric character, Enter valid email id.')


    def create(self, validated_data):
        self.clean_email(validated_data.get('email'))
        test_info = PracticeTestInfo.objects.filter(
            email=validated_data.get('email', None), order_item=None
        ).first()
        completed_test_info = PracticeTestInfo.objects.filter(
            email=validated_data.get('email', None)
        ).exclude(order_item=None).first()
        if completed_test_info:
            validated_data['test_data'] = completed_test_info.test_data
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

    def get_cefr_level(self, obj):
        level = 'N.A'
        data = getattr(obj, 'test_data', '{}')
        if data:
            data = eval(data)
            result = data.get('result', {})
            level = result.get('pt_level', 'N.A')
        return level
