
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework import status

from partner.models import  Vendor,Certificate
from shop.models import Skill,Product
from partner.models import ProductSkill
from django.utils.text import slugify
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated


class VendorCertificateMappingApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = None
    pagination_class = None

    def get(self, request, *args, **kwargs):
        new_skill_product = {}
        vendors = self.request.GET.get('name','')
        if not vendors:
            return Response({'error':'Please provide the vendor'},status=status.HTTP_400_BAD_REQUEST)

        vendors = vendors.split(',')
        vendors = Vendor.objects.only('id','slug').filter(slug__in=vendors)
        if not vendors.exists():
            return Response({'error':'No vendor Found'},status=status.HTTP_400_BAD_REQUEST)
        certificates = Certificate.objects.filter(vendor_provider__in=vendors)
        if not certificates.exists():
            return Response({'error':'No certificates found'},status=status.HTTP_400_BAD_REQUEST)
        new_list = []
        new_dict = {}
        new_skill_dict = {}

        for vendor in vendors:
            new_dict.update({vendor.id:vendor.slug})

        skills_names = certificates.values_list('skill',flat=True)
        skills_names = ",".join(skills_names)
        skills_names = list(map(lambda x: slugify(x), skills_names.split(',')))
        skills = Skill.objects.filter(slug__in=skills_names)

        for skill in skills:
            new_skill_dict.update({skill.id:skill.slug})

        product_skill = ProductSkill.objects.filter(skill_id__in=list(new_skill_dict.keys()),
                                                    product__vendor__in=vendors)
        for ps in product_skill:
            val = new_skill_product.get(new_skill_dict[ps.skill_id],[])
            val.append(ps.product_id)
            new_skill_product.update({new_skill_dict[ps.skill_id]: val})

        product_vendor = Product.objects.only('id','vendor_id').filter(vendor__in=vendors)
        prod_vendor = {}
        for prdvend in product_vendor:
            val = prod_vendor.get(prdvend.vendor_id,[])
            val.append(prdvend.id)
            prod_vendor.update({prdvend.vendor_id:val})

        for certificate in certificates:
            skills = certificate.skill.split(',')
            # skills = list(map(lambda x: slugify(x), certificate.skill.split(',')))
            new_skill = []
            for skill in skills:
                prods = set(new_skill_product.get(slugify(skill),[]))
                vendor_prod = prod_vendor.get(certificate.vendor_provider_id,{})
                prods = list(prods.intersection(vendor_prod))
                new_skill.append({'name':skill,'product_id':prods})

            new_list.append({'name':new_dict[certificate.vendor_provider_id],'certificate_set':[{
                'name':certificate.name,'skill':new_skill}]})
        return Response({'data':new_list},status=status.HTTP_200_OK)









