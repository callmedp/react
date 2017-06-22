from console.order.partials.views import NewOrdersListPartial, ClosedOrdersListPartial, HeldOrdersListPartial, NewOrdersDetailPartial, ClosedOrdersDetailPartial, HeldOrdersDetailPartial, NewOrdersUpdatableDetailPartial, ClosedOrdersUpdatableDetailPartial, HeldOrdersUpdatableDetailPartial

class NewOrdersListView(NewOrdersListPartial):

    template_name = 'console/order/pages/console-page.html'


class ClosedOrdersListView(ClosedOrdersListPartial):

    template_name = 'console/order/pages/console-page.html'


class HeldOrdersListView(HeldOrdersListPartial):

    template_name = 'console/order/pages/console-page.html'


class NewOrdersDetailView(NewOrdersDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class ClosedOrdersDetailView(ClosedOrdersDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class HeldOrdersDetailView(HeldOrdersDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class NewOrdersUpdatableDetailView(NewOrdersUpdatableDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class ClosedOrdersUpdatableDetailView(ClosedOrdersUpdatableDetailPartial):

    template_name = 'console/order/pages/console-page.html'


class HeldOrdersUpdatableDetailView(HeldOrdersUpdatableDetailPartial):

    template_name = 'console/order/pages/console-page.html'
