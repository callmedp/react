# from django.conf.urls import url, include
from django.urls import re_path, include

from .views import ConsoleLoginView, ConsoleDashboardView, ConsoleLogoutView, \
    ConsoleResetPasswordView, ConsoleAutoLoginView
from . import (
    shop_view, vendor_view, blog_view, order_view,
    refund_view, wallet_view, university_views, product_skill_view)
from geolocation import adminviews

app_name = 'console'
urlpatterns = [
    re_path(r'^cms/', include('console.cms.urls', namespace='cms')),
    re_path(r'^order/', include('console.order.urls', namespace='order')),
    re_path(r'^partner/', include('console.partner.urls', namespace='partner')),
    re_path(r'^operations/', include('console.operations.urls', namespace='operations')),
    re_path(r'^userquery/', include('console.userquery.urls', namespace='userquery')),
    re_path(r'^tasks/',
        include('console.schedule_tasks.urls', namespace='tasks')),
    re_path(r'^badge/',
        include('console.badgeuser.urls', namespace='badge')),
    re_path(r'^welcomecall/',
        include('console.welcomecall.urls', namespace='welcomecall')),
    re_path(r'^feedbackcall/',
        include('console.feedbackCall.urls', namespace='feedbackcall')),
    re_path(r'^wallet/$', wallet_view.WalletView.as_view(), name='walletrewards'),
    re_path(r'^wallet/history/$', wallet_view.WalletHistoryView.as_view(), name='wallethistory'),
    re_path(r'^api/', include('console.api.urls', namespace='api')),
    re_path(r'^compliance-report/$', order_view.ComplianceReport.as_view(), name='compliance-report'),
    re_path(r'^ltv-report/$', order_view.LTVReportView.as_view(), name='ltv-report'),

]


urlpatterns += [
    re_path(r'^$', ConsoleDashboardView.as_view(), name='dashboard'),
    re_path(r'^login/$', ConsoleLoginView.as_view(), name='login'),
    re_path(r'^reset-password/$', ConsoleResetPasswordView.as_view(), name='reset-password'),
    re_path(r'^logout/$', ConsoleLogoutView.as_view(), name='logout'),
    re_path(r'^autologin/$', ConsoleAutoLoginView.as_view(), name='autologin')
]


# search order url
# urlpatterns += [
#     re_path(r'^search/order/$',
#         order_view.SearchOrderView.as_view(),
#         name='search-order'),
# ]

# url for skills
urlpatterns += [

    re_path(r'^university/faculty/list/$',
        university_views.FacultyListView.as_view(),
        name='faculty-list'),
    re_path(r'^university/faculty/add/$',
        university_views.FacultyAddView.as_view(),
        name='faculty-add'),
    re_path(r'^university/faculty/change/(?P<pk>[\d]+)/$',
        university_views.FacultyChangeView.as_view(),
        name='faculty-change'),
]

# url for skills
urlpatterns += [

    re_path(r'^skill/autocomplete/$',
        shop_view.SkillAutocompleteView.as_view(),
        name='skill-autocomplete'),
    re_path(r'^skill/add/$',
        shop_view.SkillAddView.as_view(), name='skill-add'),
    re_path(r'^productskill/add/$',
        product_skill_view.ProductSkillAddView.as_view(),
        name='productskill-add'),
    re_path(r'^skill/list/$',
        shop_view.SkillListView.as_view(),
        name='skill-list'),
    re_path(r'^skill/change/(?P<pk>[\d]+)/$',
        shop_view.SkillChangeView.as_view(),
        name='skill-change'),
]


urlpatterns += [
    re_path(r'^screenproduct/list/$',
        vendor_view.ListScreenProductView.as_view(),
        name='screenproduct-list'),
    re_path(r'^screenproduct/add/$',
        vendor_view.AddScreenProductView.as_view(),
        name='screenproduct-add'),
    re_path(r'^screenproduct/change/(?P<pk>[\d]+)/$',
        vendor_view.ChangeScreenProductView.as_view(),
        name='screenproduct-change'),
    re_path(r'^screenproduct/variantadd/(?P<pk>[\d]+)/$',
        vendor_view.AddScreenProductVariantView.as_view(),
        name='screenproductvariant-add'),
    re_path(r'^screenproduct/variantchange/(?P<pk>[\d]+)/(?P<parent>[\d]+)/$',
        vendor_view.ChangeScreenProductVariantView.as_view(),
        name='screenproductvariant-change'),
    re_path(r'^screenproduct/moderation-list/$',
        vendor_view.ListModerationScreenProductView.as_view(),
        name='screenproduct-moderationlist'),
    re_path(r'^screenproduct/action/(?P<action>[\w-]+)/$',
        vendor_view.ActionScreenProductView.as_view(),
        name='screenproduct-action'),

    re_path(r'^screenfaq/list/$',
        vendor_view.ListScreenFaqView.as_view(),
        name='screenfaq-list'),
    re_path(r'^screenfaq/add/$',
        vendor_view.AddScreenFaqView.as_view(),
        name='screenfaq-add'),
    re_path(r'^screenfaq/change/(?P<pk>[\d]+)/$',
        vendor_view.ChangeScreenFaqView.as_view(),
        name='screenfaq-change'),
    re_path(r'^screenfaq/moderation-list/$',
        vendor_view.ListModerationScreenFaqView.as_view(),
        name='screenfaq-moderationlist'),
    re_path(r'^screenfaq/action/(?P<action>[\w-]+)/$',
        vendor_view.ActionScreenFaqView.as_view(),
        name='screenfaq-action'),
    
]

urlpatterns += [
    re_path(r'^category/add/$',
        shop_view.AddCategoryView.as_view(),
        name='category-add'),

    re_path(r'^subcategory/add/$',
        shop_view.AddSubCategoryView.as_view(),
        name='subcategory-add'),

    re_path(r'^category/list/$',
        shop_view.ListCategoryView.as_view(),
        name='category-list'),
    re_path(r'^subcategory/list/$',
        shop_view.ListSubCategoryView.as_view(),
        name='subcategory-list'),
    re_path(r'^changesubcategory/change/(?P<pk>[\d]+)/$',
        shop_view.SubCategoryChangeView.as_view(),
        name='changesubcategory-list'),


    re_path(r'^categoryrelationship/list/$',
        shop_view.ListCategoryRelationView.as_view(),
        name='category-relation-list'),
    re_path(r'^category/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeCategoryView.as_view(),
        name='category-change'),
    re_path(r'^category/action/(?P<action>[\w-]+)/$',
        shop_view.ActionCategoryView.as_view(),
        name='category-action'),
    re_path(r'^fa/list/$',
        shop_view.FunctionalAreaListView.as_view(),
        name='fa-list'),
    re_path(r'^fa/change/(?P<pk>[\d]+)/$',
        shop_view.FaChangeView.as_view(),
        name='change-fa'),
    re_path(r'^fa/create/$',
        shop_view.FaCreateView.as_view(),
        name='create-fa'),

    re_path(r'^job-title/list/$',
        shop_view.JobTitleListView.as_view(),
        name='product-job-title'),

    re_path(r'^job-title/change/(?P<pk>[\d]+)/$',
        shop_view.JobTitleChangeView.as_view(),
        name='change-job-title'),

    re_path(r'^job-title/create/$',
        shop_view.JobTitleCreateView.as_view(),
        name='create-job-title'),


    re_path(r'^product/list/$',
        shop_view.ListProductView.as_view(), name='product-list'),
    re_path(r'^product/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeProductView.as_view(), name='product-change'),
    re_path(r'^product/change-ops/(?P<pk>[\d]+)/$',
        shop_view.OPChangeProductView.as_view(), name='product-opschange'),
    re_path(r'^product/variantchange/(?P<pk>[\d]+)/(?P<parent>[\d]+)/$',
        shop_view.ChangeProductVariantView.as_view(),
        name='productvariant-change'),
    re_path(r'^product/action/(?P<action>[\w-]+)/$',
        shop_view.ActionProductView.as_view(),
        name='product-action'),
    re_path(r'product-audit-history/$',
        shop_view.ProductAuditHistoryView.as_view(),
        name='product-audit-history'),

    re_path(r'product-audit-history/download$',
        shop_view.ProductHistoryLogDownloadView.as_view(),
        name='product-audit-history-download'),

    re_path(r'^discount-report-download/$', 
        shop_view.DownloadDiscountReportView.as_view(), name='discount-report-download'),
    
    re_path(r'^upsell-report-download/$', 
        shop_view.DownloadUpsellReportView.as_view(), name='upsell-report-download'),

    re_path(r'^faq/list/$',
        shop_view.ListFaqView.as_view(),
        name='faq-list'),
    re_path(r'^faq/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeFaqView.as_view(),
        name='faquestion-change'),

    re_path(r'^keyword/add/$',
        shop_view.AddKeywordView.as_view(),
        name='keyword-add'),
    re_path(r'^keyword/list/$',
        shop_view.ListKeywordView.as_view(),
        name='keyword-list'),
    re_path(r'^keyword/change/(?P<pk>[\d]+)/$',
        shop_view.ChangeKeywordView.as_view(),
        name='keyword-change'),

    

    # re_path(r'^attribute/add/$',
    #     shop_view.AddAttributeView.as_view(),
    #     name='attribute-add'),
    # re_path(r'^attribute/list/$',
    #     shop_view.ListAttributeView.as_view(),
    #     name='attribute-list'),
    # re_path(r'^attribute/change/(?P<pk>[\d]+)/$',
    #     shop_view.ChangeAttributeView.as_view(),
    #     name='attribute-change'),

    # re_path(r'^attributeoption/add/$',
    #     shop_view.AddAttributeOptionView.as_view(),
    #     name='attributeoption-add'),
    # re_path(r'^attributeoption/list/$',
    #     shop_view.ListAttributeOptionGroupView.as_view(),
    #     name='attributeoption-list'),
]


urlpatterns += [
    re_path(r'^blog/tag/$',
        blog_view.TagListView.as_view(), name='blog-tag-list'),
    re_path(r'^blog/tag/add/$',
        blog_view.TagAddView.as_view(), name='blog-tag-add'),
    re_path(r'^blog/tag/(?P<pk>\d+)/change/$', blog_view.TagUpdateView.as_view(),
        name='blog-tag-update'),

    re_path(r'^blog/category/$', blog_view.CategoryListView.as_view(),
        name='blog-category-list'),
    re_path(r'^blog/category/add/$', blog_view.CategoryAddView.as_view(),
        name='blog-category-add'),
    re_path(r'^blog/category/(?P<pk>\d+)/change/$',
        blog_view.CategoryUpdateView.as_view(), name='blog-category-update'),

    re_path(r'^blog/article/$', blog_view.ArticleListView.as_view(),
        name='blog-article-list'),
    re_path(r'^blog/article/add/$', blog_view.ArticleAddView.as_view(),
        name='blog-article-add'),
    re_path(r'^blog/article/(?P<pk>\d+)/change/$',
        blog_view.ArticleUpdateView.as_view(), name='blog-article-update'),

    re_path(r'^blog/comment/comment-to-moderate/$',
        blog_view.CommentModerateListView.as_view(),
        name='blog-comment-to-moderate'),
    re_path(r'^blog/comment/(?P<pk>\d+)/change/$',
        blog_view.CommentModerateView.as_view(),
        name='blog-comment-moderate-update'),

    re_path(r'^blog/author/$', blog_view.AuthorListView.as_view(),
        name='blog-author-list'),
    re_path(r'^blog/author/add/$', blog_view.AuthorAddView.as_view(),
        name='blog-author-add'),
    re_path(r'^blog/author/(?P<pk>\d+)/change/$',
        blog_view.AuthorUpdateView.as_view(), name='blog-author-update'),
]


urlpatterns += [
    re_path(r'^geolocation/country/$',
        adminviews.CountryListView.as_view(), name='geo-country'),

    re_path(r'^geolocation/country/(?P<pk>\d+)/change/$',
        adminviews.CountryUpdateView.as_view(), name='geo-country-update'),
]


urlpatterns += [
    re_path(r'^queue/resumedownload/$',
        order_view.ConsoleResumeDownloadView.as_view(), name='queue-resume-download'),
    re_path(r'^queue/orders/$',
        order_view.OrderListView.as_view(), name='queue-order'),

    # re_path(r'^queue/welcomecall/$',
    #     order_view.WelcomeCallVeiw.as_view(), name='queue-welcome'),

    re_path(r'^queue/midout/$',
        order_view.MidOutQueueView.as_view(), name='queue-midout'),
    re_path(r'^queue/inbox/$',
        order_view.InboxQueueVeiw.as_view(), name='queue-inbox'),

    re_path(r'^queue/replaced-order/$',
        order_view.ReplacedOrderListView.as_view(), name='replaced-order'),

    re_path(r'^queue/approval/$',
        order_view.ApprovalQueueVeiw.as_view(), name='queue-approval'),

    re_path(r'^queue/approved/$',
        order_view.ApprovedQueueVeiw.as_view(), name='queue-approved'),

    re_path(r'^queue/rejectedbyadmin/$',
        order_view.RejectedByAdminQueue.as_view(),
        name='queue-rejectedbyadmin'),

    re_path(r'^queue/rejectedbycandidate/$',
        order_view.RejectedByCandidateQueue.as_view(),
        name='queue-rejectedbycandidate'),

    re_path(r'^queue/allocated/$',
        order_view.AllocatedQueueVeiw.as_view(), name='queue-allocated'),

    re_path(r'^queue/booster/$',
        order_view.BoosterQueueVeiw.as_view(), name='queue-booster'),

    re_path(r'^queue/whatsapplist/$',
        order_view.WhatsappListQueueView.as_view(),
        name='queue-whatsappjoblist'),

    re_path(r'^queue/whatsapp/(?P<pk>\d+)/schedule$',
        order_view.WhatsAppScheduleView.as_view(),
        name='queue-whatsapp-schedule'),

    re_path(r'^queue/certification-queue/$',
        order_view.CertficationProductQueueView.as_view(),
        name='queue-certification'),

    re_path(r'^queue/domesticprofileupdate/$',
        order_view.DomesticProfileUpdateQueueView.as_view(),
        name='queue-domesticprofileupdate'),

    re_path(r'^queue/domesticprofileinitiated/$',
        order_view.DomesticProfileInitiatedQueueView.as_view(),
        name='queue-domesticprofileinitiated'),

    re_path(r'^queue/domesticprofileapproval/$',
        order_view.DomesticProfileApprovalQueue.as_view(),
        name='queue-domesticprofileapproval'),

    re_path(r'^queue/closed/orderitems/$',
        order_view.ClosedOrderItemQueueVeiw.as_view(),
        name='queue-closed-orderitems'),

    re_path(r'^queue/orderitem/(?P<pk>\d+)/detail/$',
        order_view.OrderItemDetailVeiw.as_view(), name='order-item-detail'),

    re_path(r'^queue/order/(?P<pk>\d+)/details/$',
        order_view.OrderDetailView.as_view(), name='order-detail'),

    re_path(r'^queue/orderitem/action/$',
        order_view.ActionOrderItemView.as_view(),
        name='action-orderitem-view'),

    re_path(r'^queue/orderitem/assignment/$',
        order_view.AssignmentOrderItemView.as_view(),
        name='assignment-orderitem-view'),

    re_path(r'^queue/testimonial/testimonial-list/$',
        order_view.TestimonialListView.as_view(),
        name='testimonial-list'),

    re_path(r'^queue/testimonial/testimonial-add-new/$',
        order_view.CreateTestimonialView.as_view(),
        name='testimonial-add-new'),

    re_path(r'^queue/testimonial/testimonial/(?P<pk>\d+)/update/$',
        order_view.UpdateTestimonialView.as_view(),
        name='testimonial-update'),

    re_path(r'^queue/review/review-to-moderate/$',
        order_view.ReviewModerateListView.as_view(),
        name='review-to-moderate'),

    re_path(r'^queue/review/(?P<pk>\d+)/change/$',
        order_view.ReviewModerateView.as_view(),
        name='review-moderate-update'),
]

# refunf flow
urlpatterns += [
    re_path(r'^refund/refundrequest/$',
        refund_view.RefundOrderRequestView.as_view(),
        name='refund-request'),

    re_path(r'^refund/refundrequestapproval/$',
        refund_view.RefundRequestApprovalView.as_view(),
        name='refund-request-approval'),

    re_path(r'^refund/refundraise/$',
        refund_view.RefundRaiseRequestView.as_view(),
        name='refund-raiserequest'),

    re_path(r'^refund/validatecheckeditems/$',
        refund_view.ValidateCheckedItems.as_view(),
        name='refund-validateitems'),

    re_path(r'^refund/validateuncheckeditems/$',
        refund_view.ValidateUnCheckedItems.as_view(),
        name='refund-validateitems'),

    re_path(r'^refund/refundrequest-detail/(?P<pk>\d+)/$',
        refund_view.RefundRequestDetail.as_view(),
        name='refundrequest-detail'),

    re_path(r'^refund/refundrequest/(?P<pk>\d+)/edit/$',
        refund_view.RefundRequestEditView.as_view(),
        name='refundrequest-edit'),

    # re_path(r'^refund/sendforapproval-refundrequest/',
    #     refund_view.SendForApprovalRefundRequest.as_view(),
    #     name='sendforapproval-refundrequest'),

    re_path(r'^refund/reject-refundrequest/',
        refund_view.RejectRefundRequestView.as_view(),
        name='refundrequest-reject'),

    re_path(r'^refund/approve-refundrequest/',
        refund_view.ApproveRefundRequestView.as_view(),
        name='refundrequest-approve'),

    re_path(r'^refund/cancel-refundrequest/',
        refund_view.CancelRefundRequestView.as_view(),
        name='refundrequest-cancel'),

]

from . import linkedin_view

urlpatterns += [
    re_path(r'^counselling-listing/(?P<ord_pk>[-\w]+)/$',
        linkedin_view.ListCounsellingFormView.as_view(), name='counselling-list'),

    re_path(r'^linkedin/inbox/$',
        linkedin_view.LinkedinQueueView.as_view(),
        name='linkedin-inbox'),

    re_path(r'^linkedin/change-draft/(?P<pk>\d+)/draft/$',
        linkedin_view.ChangeDraftView.as_view(),
        name='change-draft'),

    re_path(r'^linkedin/create/(?P<oi>\d+)/draft/$',
        linkedin_view.CreateDrftObject.as_view(),
        name='create-draft'),

    re_path(r'^linkedin/order/(?P<pk>\d+)/detail/$',
        linkedin_view.LinkedinOrderDetailVeiw.as_view(), name='linkedin-order-detail'),

    re_path(r'^linkedin/rejected-by-admin/$',
        linkedin_view.LinkedinRejectedByAdminView.as_view(),
        name='linkedin-rejectedbylinkedinadmin'),

    re_path(r'^linkedin/rejectedbycandidate/$',
        linkedin_view.LinkedinRejectedByCandidateView.as_view(),
        name='linkedin-rejectedbylinkedincandidate'),

    re_path(r'^linkedin/linkedin-approval/$',
        linkedin_view.LinkedinApprovalVeiw.as_view(),
        name='linkedin-approval'),

    re_path(r'^linkedin/linkedin-approved-queue/$',
        linkedin_view.ApprovedLinkedinQueueVeiw.as_view(),
        name='linkedin-approved-queue'),

    re_path(r'^queue/internationalprofileupdate/$',
        linkedin_view.InterNationalUpdateQueueView.as_view(),
        name='queue-internationalprofileupdate'),

    re_path(r'^queue/internationalapproval/$',
        linkedin_view.InterNationalApprovalQueue.as_view(),
        name='queue-internationalapproval'),

    re_path(r'^queue/orderitem/internationalassignment/$',
        linkedin_view.InterNationalAssignmentOrderItemView.as_view(),
        name='international-assignment-orderitem-view'),

    re_path(r'^queqe/internationalprofile/(?P<pk>\d+)/update/$',
        linkedin_view.ProfileUpdationView.as_view(), name='international_profile_update'),

    re_path(r'^queqe/profile-credentials/(?P<oi>\d+)/download/$',
        linkedin_view.ProfileCredentialDownload.as_view(), name='profile_credentials'), 
]

