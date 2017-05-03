from console.cms.partials.views import PageListPartial, CommentListPartial, PageDetailPartial, PageAddPartial


class PageListView(PageListPartial):

    template_name = 'cms/pages/console-page.html'


class CommentListView(CommentListPartial):

    template_name = 'cms/pages/console-page.html'


class PageDetailView(PageDetailPartial):

    template_name = 'cms/pages/console-page.html'


class PageAddView(PageAddPartial):

    template_name = 'cms/pages/console-page.html'