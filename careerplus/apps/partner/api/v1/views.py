
# third party import
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# inter-app import
from partner.api.core.mixins import VendorViewMixin, VendorHierarchyViewMixin
from .serializers import VendorListSerializer
from partner.models import Vendor
from shared.rest_addons.mixins import FieldFilterMixin
from partner.mixins import VendorUrlMixins
from shop.models import Product

class VendorViewSet(VendorViewMixin, ModelViewSet):
    """
        CRUD Viewset for `Vendor` model.
    """


class VendorHierarchyViewSet(VendorHierarchyViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `VendorHierarchy` model.
    """



class VendorListApiView(FieldFilterMixin, ListAPIView):
    """
    Get Vendor List Api End point
    """
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = VendorListSerializer

class VendorUrlApiView(APIView):
    """
    """
    serializer_class = None
    authentication_classes = ()
    permission_classes = ()

    def normalize_dict(self, data_dict):
        for value in data_dict:
            if isinstance(data_dict[value], list):
                data_dict[value] = data_dict[value][0]
        return data_dict

    def post(self, request, *args, **kwargs):
        """
        """
        data_dict = dict(request.data)
        data_dict = self.normalize_dict(data_dict=data_dict)
        course_id = data_dict.get('course_id', 0)
        vendor_slug = None
        try:
            product = Product.objects.filter(id=course_id).first()

            if product:
                vendor = product.vendor
                vendor_slug = vendor.slug
        except Exception as e:
            return Response({"vendor_url":""}, status=status.HTTP_200_OK)

        if not vendor_slug:
            return Response({"vendor_url":""}, status=status.HTTP_200_OK)

        site_url = VendorUrlMixins().get_vendor_mapping(vendor_slug=vendor_slug, data_dict=data_dict)
        #site_url = "http://lms.iselglobal.in/index.aspx?e=sahil.singla@hindustantimes.com&p=F9F77FB3-9710-48A6-924E-4FB6C0ACF0C6"
        if isinstance(site_url, dict):
            if site_url.get('error_message', ''):
                return Response(site_url, status=status.HTTP_400_BAD_REQUEST)  
        return Response({"vendor_url": site_url}, status=status.HTTP_200_OK)
