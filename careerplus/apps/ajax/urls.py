from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'ajax'
urlpatterns = [
    url(r'^page/load-more/$',
        views.AjaxCommentLoadMoreView.as_view(), name='comment-load-more'),

    url(r'^university-skill-course/loadmore/$',
        views.UniversityCourseLoadMoreView.as_view(),
        name='university-course-load-more'),

    url(r'^page/cms-share/$',
        views.CmsShareView.as_view(), name='cms-share'),

    url(r'^product/load-more/$',
        views.AjaxProductLoadMoreView.as_view(), name='product-load-more'),

    url(r'^review/load-more/$',
        views.AjaxReviewLoadMoreView.as_view(), name='review-load-more'),

    url(r'^article-share/$',
        views.ArticleShareView.as_view(), name='article-share'),

    url(r'^article-comment/$',
        views.ArticleCommentView.as_view(), name='article-comment-post'),

    url(r'^email-exist/$',
        views.EmailExistView.as_view(), name='email-exist'),

    url(r'^get-states/$',
        views.AjaxStateView.as_view(), name='indian-state'),

    # auto login token for shine profile update
    url(r'^autologin/tokengenerator/$',
        views.GenerateAutoLoginToken.as_view(), name='autologin-tokengenerate'),

    # custom admin flow
    url(r'^orderitem/add-comment/$',
        views.AjaxOrderItemCommentView.as_view(), name='order-item-comment'),

    url(r'^orderitem/approve-draft/$',
        views.ApproveByAdminDraft.as_view(), name='oi-draft-accept'),

    url(r'^orderitem/reject-draft/$',
        views.RejectByAdminDraft.as_view(), name='oi-draft-reject'),

    url(r'^orderitem/upload-draft/$',
        views.UploadDraftView.as_view(), name='oi-draft-upload'),

    url(r'^orderitem/detaii-page-upload-draft/$',
        views.DetailPageUploadDraftView.as_view(), name='detaii-page-upload-draft'),

    url(r'^orderitem/waiting-input-save/$',
        views.SaveWaitingInput.as_view(), name='oi-waiting-input'),

    url(r'^orderitem/linkedin-approve-draft/$',
        views.ApproveDraftByLinkedinAdmin.as_view(), name='linkedin-approve-draft'),

    url(r'^orderitem/linkedin-reject-draft/$',
        views.RejectDraftByLinkedinAdmin.as_view(), name='linkedin-reject-draft'),

    url(r'^order/markedpaid/$',
        views.MarkedPaidOrderView.as_view(), name='order-markedpaid'),

    url(r'^order/orderlistmodal/$',
        views.OrderListModal.as_view(), name='order-orderlistmodal'),

    url(r'^get-ltv/$',
        csrf_exempt(views.GetLTVAjaxView.as_view()), name='bulk-ltv-view'),


    #welcome call direct

    url(r'^service-call/$', csrf_exempt(views.WelcomeServiceCallView.as_view()), name='wcservice-call'),

    #duplicateproductcreation
    url(r'^copy-product/$', csrf_exempt(views.ProductCopyAPIView.as_view()), name='product-copy'),

]
