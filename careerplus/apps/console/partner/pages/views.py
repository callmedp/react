from console.partner.partials.views import VendorListPartial, VendorHierarchyListPartial, VendorDetailPartial, VendorHierarchyDetailPartial, VendorAddPartial, VendorHierarchyAddPartial, NewOrdersListPartial, ClosedOrdersListPartial, HeldOrdersListPartial,NewOrdersDetailPartial, ClosedOrdersDetailPartial, HeldOrdersDetailPartial

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


class NewOrdersListView(NewOrdersListPartial):

    template_name = 'console/partner/pages/console-page.html'


class ClosedOrdersListView(ClosedOrdersListPartial):

    template_name = 'console/partner/pages/console-page.html'


class HeldOrdersListView(HeldOrdersListPartial):

    template_name = 'console/partner/pages/console-page.html'


class NewOrdersDetailView(NewOrdersDetailPartial):

    template_name = 'console/partner/pages/console-page.html'


class ClosedOrdersDetailView(ClosedOrdersDetailPartial):

    template_name = 'console/partner/pages/console-page.html'


class HeldOrdersDetailView(HeldOrdersDetailPartial):

    template_name = 'console/partner/pages/console-page.html'
