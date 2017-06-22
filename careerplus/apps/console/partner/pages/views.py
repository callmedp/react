from console.partner.partials.views import VendorListPartial, VendorHierarchyListPartial, VendorDetailPartial, VendorHierarchyDetailPartial, VendorAddPartial, VendorHierarchyAddPartial


class VendorListView(VendorListPartial):

    template_name = 'console/partner/pages/console-page.html'


class VendorHierarchyListView(VendorHierarchyListPartial):

    template_name = 'console/partner/pages/console-page.html'


class VendorDetailView(VendorDetailPartial):

    template_name = 'console/partner/pages/console-page.html'


class VendorHierarchyDetailView(VendorHierarchyDetailPartial):

    template_name = 'console/partner/pages/console-page.html'


class VendorAddView(VendorAddPartial):

    template_name = 'console/partner/pages/console-page.html'


class VendorHierarchyAddView(VendorHierarchyAddPartial):

    template_name = 'console/partner/pages/console-page.html'
