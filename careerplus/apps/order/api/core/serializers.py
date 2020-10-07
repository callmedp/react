from rest_framework import serializers
from order import models
from users.models import User
from shop.api.core.serializers import ProductSerializer
from rest_framework import  serializers
from shared.rest_addons.mixins import SerializerFieldsMixin, ListSerializerContextMixin, ListSerializerDataMixin


class OrderSerializer(serializers.ModelSerializer):
	"""
		Serializer for `Order` model
	"""
	class Meta:
		model = models.Order
		fields = '__all__'
		read_only_fields = ('id', 'number', 'site', 'cart', 'candidate_id', 'txn', 'instrument_number', 'instrument_issuer', 'instrument_issue_date', 'payment_mode', 'payment_date', 'currency', 'total_incl_tax', 'total_excl_tax', 'date_placed', 'email', 'first_name', 'last_name', 'country_code', 'mobile', 'address', 'pincode', 'state', 'country')


class OrderItemSerializer(serializers.ModelSerializer):
	"""
		Serializer for `OrderItem` model
	"""
	order = OrderSerializer()
	product = ProductSerializer()
	class Meta:
		model = models.OrderItem
		fields = '__all__'
		read_only_fields = ('id',)


class OrderItemOperationsSerializer(SerializerFieldsMixin,
					ListSerializerContextMixin, ListSerializerDataMixin,
									serializers.ModelSerializer):
	"""
	Serailzer for OrderItem operations

	"""
	list_lookup_fields = ['oi_id','added_by_id','assigned_to_id']
	fields_required_mapping = {'oi_id':['no_process','oi_draft_path',],
							   'added_by_id':['name'],
							   'assigned_to_id': ['name'],
							   }
	field_model_mapping = {'oi_id': models.OrderItem,
						   'added_by_id': User,
						   'assigned_to_id':User,
						   }

	oi_status_display = serializers.CharField(read_only=True)
	# oi_resume_name = serializers.SerializerMethodField('get_oi_resume_name',read_only=True)
	# oi_draft_name = serializers.SerializerMethodField('get_oi_draft_name',read_only=True)


	# def oi_resume_name(self,obj):
	# 	if not obj:
	# 		return ''
	# 	return obj.oi_resume.name if obj.oi_resume else ''
	#
	# def oi_draft_name(self,obj):
	# 	if not obj:
	# 		return ''
	# 	return obj.oi_draft.name if obj.oi_draft else ''


	class Meta:
		model = models.OrderItemOperation
		fields = '__all__'
		ordering = ['created']


class MessageCommunincationSerializer(SerializerFieldsMixin,
									  serializers.ModelSerializer):
	""""
	Serializer for message communications
	"""

	added_by_name = serializers.CharField()

	class Meta:
		model = models.Message
		fields = "__all__"
