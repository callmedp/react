



#inter app imports 
from coupon.models import Coupon


#third party imports 
from rest_framework import serializers


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
