from django.conf.urls import url, include

from .views import ConsoleLoginView, ConsoleDashboardView, ConsoleLogoutView, \
    ConsoleResetPasswordView, ConsoleAutoLoginView
from . import (
    shop_view, vendor_view, blog_view, order_view,
    refund_view, wallet_view, university_views, product_skill_view)
from geolocation import adminviews


urlpatterns = [
    url(r'^cms/', include('console.cms.urls', namespace='cms')),
    url(r'^order/', include('console.order.urls', namespace='order')),
    url(r'^partner/', include('console.partner.urls', namespace='partner')),
    url(r'^operations/', include('console.operations.urls', namespace='operations')),
    url(r'^userquery/', include('console.userquery.urls', namespace='userquery')),
    url(r'^tasks/',
        include('console.schedule_tasks.urls', namespace='tasks')),
    url(r'^badge/',
        include('console.badgeuser.urls', namespace='badge')),
    url(r'^welcomecall/',
        include('console.welcomecall.urls', namespace='welcomecall')),
    url(r'^wallet/$', wallet_view.WalletView.as_view(), name='walletrewards'),
    url(r'^wallet/history/$', wallet_view.WalletHistoryView.as_view(), name='wallethistory'),
    url(r'^api/', include('console.api.urls', namespace='api')),
    url(r'^compliance-report/$', order_view.ComplianceReport.as_view(), name='compliance-report'),

]


urlpatterns += [
    url(r'^$', ConsoleDashboardView.as_view(), name='dashboard'),
    url(r'^login/$', ConsoleLoginView.as_view(), name='login'),
    url(r'^reset-password/$', ConsoleResetPasswordView.as_view(), name='reset-password'),
    url(r'^logout/$', ConsoleLogoutView.as_view(), name='logout'),
    url(r'^autologin/$', ConsoleAutoLoginView.as_view(), name='autologin')
]


# search order url
# urlpatterns += [
#     url(r'^search/order/$',
#         order_view.SearchOrderView.as_view(),
#         name='search-order'),
# ]

# url for skills
urlpatterns += [

    url(r'^university/faculty/list/$',
        university_views.FacultyListView.as_view(),
        name='faculty-list'),
    url(r'^university/faculty/add/$',
        university_views.FacultyAddView.as_view(),
        name='faculty-add'),
    url(r'^university/faculty/change/(?P<pk>[\d]+)/$',
        university_views.FacultyChangeView.as_view(),
        name='faculty-change'),
]

# url for skills
urlpatterns += [

    url(r'^skill/autocomplete/$',
        shop_view.SkillAutocompleteView.as_view(),
        name='skill-autocomplete'),
    url(r'^skill/add/$',
        shop_view.SkillAddView.as_view(), name='skill-add'),
    url(r'^productskill/add/$',
        product_skill_view.ProductSkillAddView.as_view(),
        name='productskill-add'),
    url(r'^skill/list/$',
        shop_view.SkillListView.as_view(),
        name='skill-list'),
    url(r'^skill/change/(?P<pk>[\d]+)/$',
        shop_view.SkillChangeView.as_view(),
        name='skill-change'),
]


urlpatterns += [
    url(r'^screenproduct/list/$',
        vendor_view.ListScreenProductView.as_view(),
        name='screenproduct-list'),
    url(r'^screenproduct/add/$',
        vendor_view.AddScreenProductView.as_view(),
        name='screenproduct-add'),
    url(r'^screenproduct/change/(?P<pk>[\d]+)/$',
        vendor_view.ChangeScreenProductView.as_view(),
        name='screenproduct-change'),
    url(r'^screenproduct/variantadd/(?P<pk>[\d]+)/$',
        vendor_view.AddScreenProductVariantView.as_view(),
        name='screenproductvariant-add'),
    url(r'^screenproduct/variantchange/(?P<pk>[\d]+)/(?P<parent>[\d]+)/$',
        vendor_view.ChangeScreenProductVariantView.as_view(),
        name='screenproductvariant-change'),
    url(r'^screenproduct/moderation-list/$',
        vendor_view.ListModerationScreenProductView.as_view(),
        name='screenproduct-moderationlist'),
    url(r'^screenproduct/action/(?P<action>[\w-]+)/$',
        vendor_view.ActionScreenProductView.as_view(),
        name='screenproduct-action'),

    url(r'^screenfaq/list/$',
        vendor_view.ListScreenFaqView.as_view(),
        name='screenfaq-list'),
    url(r'^screenfaq/add/$',
        vendor_view.AddScreenFaqView.as_view(),
        name='screenfaq-add'),
    url(r'^screenfaq/change/(?P<pk>[\d]+)/$',
        vendor_view.ChangeScreenFaqView.as_view(),
        name='screenfaq-change'),
    url(r'^screenfaq/moderation-list/$',
        vendor_view.ListModerationScreenFaqView.as_view(),
        name='screenfaq-moderationlist'),
    url(r'^screenfaq/action/(?P<action>[\w-]+)/$',
        vendor_view.ActionScreenFaqView.as_view(),
        name='screenfaq-action'),
    
]

urlpatterns += [
    url(r'^category/add/$',
        shop_view.AddCategoryView.as_view(),
        name='category-add'),

    url(r'^subcategory/add/$',
        shop_view.AddSubCategoryView.as_view(),
        name='subcategory-add'),

    url(r'^category/list/$',
        shop_view.ListCategoryView.as_view(),
        name='category-list'),
    url(r'^subcategory/list/$',
        shop_view.ListSubCategoryView.as_view(),
        name='subcategory-list'),
    url(r'^changesubcategory/change/(?P<pk>[\d]+)/$',
        shop_view.SubCategoryChangeView.as_view(),
        name='changesubcategory-list'),


    url(r'^categoryrelationship/list/$',
        shop_view.ListCategoryRelationView.as_view(),
        name='category-relation-list'),
    url(r'^category/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeCategoryView.as_view(),
        name='category-change'),
    url(r'^category/action/(?P<action>[\w-]+)/$',
        shop_view.ActionCategoryView.as_view(),
        name='category-action'),
    

    url(r'^product/list/$',
        shop_view.ListProductView.as_view(), name='product-list'),
    url(r'^product/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeProductView.as_view(), name='product-change'),
    url(r'^product/change-ops/(?P<pk>[\d]+)/$',
        shop_view.OPChangeProductView.as_view(), name='product-opschange'),
    url(r'^product/variantchange/(?P<pk>[\d]+)/(?P<parent>[\d]+)/$',
        shop_view.ChangeProductVariantView.as_view(),
        name='productvariant-change'),
    url(r'^product/action/(?P<action>[\w-]+)/$',
        shop_view.ActionProductView.as_view(),
        name='product-action'),
    url(r'product-audit-history/$',
        shop_view.ProductAuditHistoryView.as_view(),
        name='product-audit-history'),

    url(r'product-audit-history/download$',
        shop_view.ProductHistoryLogDownloadView.as_view(),
        name='product-audit-history-download'),

    url(r'^discount-report-download/$', 
        shop_view.DownloadDiscountReportView.as_view(), name='discount-report-download'),
    
    url(r'^upsell-report-download/$', 
        shop_view.DownloadUpsellReportView.as_view(), name='upsell-report-download'),

    url(r'^faq/list/$',
        shop_view.ListFaqView.as_view(),
        name='faq-list'),
    url(r'^faq/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeFaqView.as_view(),
        name='faquestion-change'),

    url(r'^keyword/add/$',
        shop_view.AddKeywordView.as_view(),
        name='keyword-add'),
    url(r'^keyword/list/$',
        shop_view.ListKeywordView.as_view(),
        name='keyword-list'),
    url(r'^keyword/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeKeywordView.as_view(),
        name='keyword-change'),
    

    # url(r'^attribute/add/$',
    #     shop_view.AddAttributeView.as_view(),
    #     name='attribute-add'),
    # url(r'^attribute/list/$',
    #     shop_view.ListAttributeView.as_view(),
    #     name='attribute-list'),
    # url(r'^attribute/change/(?P<pk>[\d]+)/$',
    #     shop_view.ChangeAttributeView.as_view(),
    #     name='attribute-change'),

    # url(r'^attributeoption/add/$',
    #     shop_view.AddAttributeOptionView.as_view(),
    #     name='attributeoption-add'),
    # url(r'^attributeoption/list/$',
    #     shop_view.ListAttributeOptionGroupView.as_view(),
    #     name='attributeoption-list'),
]


urlpatterns += [
    url(r'^blog/tag/$',
        blog_view.TagListView.as_view(), name='blog-tag-list'),
    url(r'^blog/tag/add/$',
        blog_view.TagAddView.as_view(), name='blog-tag-add'),
    url(r'^blog/tag/(?P<pk>\d+)/change/$', blog_view.TagUpdateView.as_view(),
        name='blog-tag-update'),

    url(r'^blog/category/$', blog_view.CategoryListView.as_view(),
        name='blog-category-list'),
    url(r'^blog/category/add/$', blog_view.CategoryAddView.as_view(),
        name='blog-category-add'),
    url(r'^blog/category/(?P<pk>\d+)/change/$',
        blog_view.CategoryUpdateView.as_view(), name='blog-category-update'),

    url(r'^blog/article/$', blog_view.ArticleListView.as_view(),
        name='blog-article-list'),
    url(r'^blog/article/add/$', blog_view.ArticleAddView.as_view(),
        name='blog-article-add'),
    url(r'^blog/article/(?P<pk>\d+)/change/$',
        blog_view.ArticleUpdateView.as_view(), name='blog-article-update'),

    url(r'^blog/comment/comment-to-moderate/$',
        blog_view.CommentModerateListView.as_view(),
        name='blog-comment-to-moderate'),
    url(r'^blog/comment/(?P<pk>\d+)/change/$',
        blog_view.CommentModerateView.as_view(),
        name='blog-comment-moderate-update'),

    url(r'^blog/author/$', blog_view.AuthorListView.as_view(),
        name='blog-author-list'),
    url(r'^blog/author/add/$', blog_view.AuthorAddView.as_view(),
        name='blog-author-add'),
    url(r'^blog/author/(?P<pk>\d+)/change/$',
        blog_view.AuthorUpdateView.as_view(), name='blog-author-update'),
]


urlpatterns += [
    url(r'^geolocation/country/$',
        adminviews.CountryListView.as_view(), name='geo-country'),

    url(r'^geolocation/country/(?P<pk>\d+)/change/$',
        adminviews.CountryUpdateView.as_view(), name='geo-country-update'),
]


urlpatterns += [
    url(r'^queue/resumedownload/$',
        order_view.ConsoleResumeDownloadView.as_view(), name='queue-resume-download'),
    url(r'^queue/orders/$',
        order_view.OrderListView.as_view(), name='queue-order'),

    # url(r'^queue/welcomecall/$',
    #     order_view.WelcomeCallVeiw.as_view(), name='queue-welcome'),

    url(r'^queue/midout/$',
        order_view.MidOutQueueView.as_view(), name='queue-midout'),
    url(r'^queue/inbox/$',
        order_view.InboxQueueVeiw.as_view(), name='queue-inbox'),

    url(r'^queue/replaced-order/$',
        order_view.ReplacedOrderListView.as_view(), name='replaced-order'),

    url(r'^queue/approval/$',
        order_view.ApprovalQueueVeiw.as_view(), name='queue-approval'),

    url(r'^queue/approved/$',
        order_view.ApprovedQueueVeiw.as_view(), name='queue-approved'),

    url(r'^queue/rejectedbyadmin/$',
        order_view.RejectedByAdminQueue.as_view(),
        name='queue-rejectedbyadmin'),

    url(r'^queue/rejectedbycandidate/$',
        order_view.RejectedByCandidateQueue.as_view(),
        name='queue-rejectedbycandidate'),

    url(r'^queue/allocated/$',
        order_view.AllocatedQueueVeiw.as_view(), name='queue-allocated'),

    url(r'^queue/booster/$',
        order_view.BoosterQueueVeiw.as_view(), name='queue-booster'),

    url(r'^queue/whatsapplist/$',
        order_view.WhatsappListQueueView.as_view(),
        name='queue-whatsappjoblist'),

    url(r'^queue/whatsapp/(?P<pk>\d+)/schedule$',
        order_view.WhatsAppScheduleView.as_view(),
        name='queue-whatsapp-schedule'),

    url(r'^queue/certification-queue/$',
        order_view.CertficationProductQueueView.as_view(),
        name='queue-certification'),

    url(r'^queue/domesticprofileupdate/$',
        order_view.DomesticProfileUpdateQueueView.as_view(),
        name='queue-domesticprofileupdate'),

    url(r'^queue/domesticprofileinitiated/$',
        order_view.DomesticProfileInitiatedQueueView.as_view(),
        name='queue-domesticprofileinitiated'),

    url(r'^queue/domesticprofileapproval/$',
        order_view.DomesticProfileApprovalQueue.as_view(),
        name='queue-domesticprofileapproval'),

    url(r'^queue/closed/orderitems/$',
        order_view.ClosedOrderItemQueueVeiw.as_view(),
        name='queue-closed-orderitems'),

    url(r'^queue/orderitem/(?P<pk>\d+)/detail/$',
        order_view.OrderItemDetailVeiw.as_view(), name='order-item-detail'),

    url(r'^queue/order/(?P<pk>\d+)/details/$',
        order_view.OrderDetailView.as_view(), name='order-detail'),

    url(r'^queue/orderitem/action/$',
        order_view.ActionOrderItemView.as_view(),
        name='action-orderitem-view'),

    url(r'^queue/orderitem/assignment/$',
        order_view.AssignmentOrderItemView.as_view(),
        name='assignment-orderitem-view'),

    url(r'^queue/review/review-to-moderate/$',
        order_view.ReviewModerateListView.as_view(),
        name='review-to-moderate'),

    url(r'^queue/review/(?P<pk>\d+)/change/$',
        order_view.ReviewModerateView.as_view(),
        name='review-moderate-update'),
]

# refunf flow
urlpatterns += [
    url(r'^refund/refundrequest/$',
        refund_view.RefundOrderRequestView.as_view(),
        name='refund-request'),

    url(r'^refund/refundrequestapproval/$',
        refund_view.RefundRequestApprovalView.as_view(),
        name='refund-request-approval'),

    url(r'^refund/refundraise/$',
        refund_view.RefundRaiseRequestView.as_view(),
        name='refund-raiserequest'),

    url(r'^refund/validatecheckeditems/$',
        refund_view.ValidateCheckedItems.as_view(),
        name='refund-validateitems'),

    url(r'^refund/validateuncheckeditems/$',
        refund_view.ValidateUnCheckedItems.as_view(),
        name='refund-validateitems'),

    url(r'^refund/refundrequest-detail/(?P<pk>\d+)/$',
        refund_view.RefundRequestDetail.as_view(),
        name='refundrequest-detail'),

    url(r'^refund/refundrequest/(?P<pk>\d+)/edit/$',
        refund_view.RefundRequestEditView.as_view(),
        name='refundrequest-edit'),

    # url(r'^refund/sendforapproval-refundrequest/',
    #     refund_view.SendForApprovalRefundRequest.as_view(),
    #     name='sendforapproval-refundrequest'),

    url(r'^refund/reject-refundrequest/',
        refund_view.RejectRefundRequestView.as_view(),
        name='refundrequest-reject'),

    url(r'^refund/approve-refundrequest/',
        refund_view.ApproveRefundRequestView.as_view(),
        name='refundrequest-approve'),

    url(r'^refund/cancel-refundrequest/',
        refund_view.CancelRefundRequestView.as_view(),
        name='refundrequest-cancel'),

]

from . import linkedin_view

urlpatterns += [
    url(r'^counselling-listing/(?P<ord_pk>[-\w]+)/$',
        linkedin_view.ListCounsellingFormView.as_view(), name='counselling-list'),

    url(r'^linkedin/inbox/$',
        linkedin_view.LinkedinQueueView.as_view(),
        name='linkedin-inbox'),

    url(r'^linkedin/change-draft/(?P<pk>\d+)/draft/$',
        linkedin_view.ChangeDraftView.as_view(),
        name='change-draft'),

    url(r'^linkedin/create/(?P<oi>\d+)/draft/$',
        linkedin_view.CreateDrftObject.as_view(),
        name='create-draft'),

    url(r'^linkedin/order/(?P<pk>\d+)/detail/$',
        linkedin_view.LinkedinOrderDetailVeiw.as_view(), name='linkedin-order-detail'),

    url(r'^linkedin/rejected-by-admin/$',
        linkedin_view.LinkedinRejectedByAdminView.as_view(),
        name='linkedin-rejectedbylinkedinadmin'),

    url(r'^linkedin/rejectedbycandidate/$',
        linkedin_view.LinkedinRejectedByCandidateView.as_view(),
        name='linkedin-rejectedbylinkedincandidate'),

    url(r'^linkedin/linkedin-approval/$',
        linkedin_view.LinkedinApprovalVeiw.as_view(),
        name='linkedin-approval'),

    url(r'^linkedin/linkedin-approved-queue/$',
        linkedin_view.ApprovedLinkedinQueueVeiw.as_view(),
        name='linkedin-approved-queue'),

    url(r'^queue/internationalprofileupdate/$',
        linkedin_view.InterNationalUpdateQueueView.as_view(),
        name='queue-internationalprofileupdate'),

    url(r'^queue/internationalapproval/$',
        linkedin_view.InterNationalApprovalQueue.as_view(),
        name='queue-internationalapproval'),

    url(r'^queue/orderitem/internationalassignment/$',
        linkedin_view.InterNationalAssignmentOrderItemView.as_view(),
        name='international-assignment-orderitem-view'),

    url(r'^queqe/internationalprofile/(?P<pk>\d+)/update/$',
        linkedin_view.ProfileUpdationView.as_view(), name='international_profile_update'),

    url(r'^queqe/profile-credentials/(?P<oi>\d+)/download/$',
        linkedin_view.ProfileCredentialDownload.as_view(), name='profile_credentials'), 
]

