# from django.conf.urls import url
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'ajax'
urlpatterns = [
    re_path(r'^page/load-more/$',
        views.AjaxCommentLoadMoreView.as_view(), name='comment-load-more'),

    re_path(r'^university-skill-course/loadmore/$',
        views.UniversityCourseLoadMoreView.as_view(),
        name='university-course-load-more'),

    re_path(r'^page/cms-share/$',
        views.CmsShareView.as_view(), name='cms-share'),

    re_path(r'^product/load-more/$',
        views.AjaxProductLoadMoreView.as_view(), name='product-load-more'),

    re_path(r'^review/load-more/$',
        views.AjaxReviewLoadMoreView.as_view(), name='review-load-more'),

    re_path(r'^article-share/$',
        views.ArticleShareView.as_view(), name='article-share'),

    re_path(r'^article-comment/$',
        views.ArticleCommentView.as_view(), name='article-comment-post'),

    re_path(r'^email-exist/$',
        views.EmailExistView.as_view(), name='email-exist'),

    re_path(r'^get-states/$',
        views.AjaxStateView.as_view(), name='indian-state'),

    # auto login token for shine profile update
    re_path(r'^autologin/tokengenerator/$',
        views.GenerateAutoLoginToken.as_view(), name='autologin-tokengenerate'),

    # custom admin flow
    re_path(r'^orderitem/add-comment/$',
        views.AjaxOrderItemCommentView.as_view(), name='order-item-comment'),

    re_path(r'^orderitem/approve-draft/$',
        views.ApproveByAdminDraft.as_view(), name='oi-draft-accept'),

    re_path(r'^orderitem/reject-draft/$',
        views.RejectByAdminDraft.as_view(), name='oi-draft-reject'),

    re_path(r'^orderitem/upload-draft/$',
        views.UploadDraftView.as_view(), name='oi-draft-upload'),

    re_path(r'^orderitem/detaii-page-upload-draft/$',
        views.DetailPageUploadDraftView.as_view(), name='detaii-page-upload-draft'),

    re_path(r'^orderitem/waiting-input-save/$',
        views.SaveWaitingInput.as_view(), name='oi-waiting-input'),

    re_path(r'^orderitem/linkedin-approve-draft/$',
        views.ApproveDraftByLinkedinAdmin.as_view(), name='linkedin-approve-draft'),

    re_path(r'^orderitem/linkedin-reject-draft/$',
        views.RejectDraftByLinkedinAdmin.as_view(), name='linkedin-reject-draft'),

    re_path(r'^order/markedpaid/$',
        views.MarkedPaidOrderView.as_view(), name='order-markedpaid'),

    re_path(r'^order/orderlistmodal/$',
        views.OrderListModal.as_view(), name='order-orderlistmodal'),

    re_path(r'^get-ltv/$',
        csrf_exempt(views.GetLTVAjaxView.as_view()), name='bulk-ltv-view'),


    #welcome call direct

    re_path(r'^service-call/$', csrf_exempt(views.WelcomeServiceCallView.as_view()), name='wcservice-call'),

    #duplicateproductcreation
    re_path(r'^copy-product/$', csrf_exempt(views.ProductCopyAPIView.as_view()), name='product-copy'),

]
