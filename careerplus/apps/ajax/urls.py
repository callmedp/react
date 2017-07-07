from django.conf.urls import url


from .views import AjaxCommentLoadMoreView, CmsShareView,\
    ArticleShareView, ArticleCommentView,\
    AjaxProductLoadMoreView, AjaxReviewLoadMoreView,\
    EmailExistView, AjaxStateView, AjaxOrderItemCommentView,\
    ApproveByAdminDraft, RejectByAdminDraft, UploadDraftView,\
    SaveWaitingInput, ApproveDraftByLinkedinAdmin, RejectDraftByLinkedinAdmin

urlpatterns = [
    url(r'^page/load-more/$',
        AjaxCommentLoadMoreView.as_view(), name='comment-load-more'),

    url(r'^page/cms-share/$',
        CmsShareView.as_view(), name='cms-share'),

    url(r'^product/load-more/$',
        AjaxProductLoadMoreView.as_view(), name='product-load-more'),

    url(r'^review/load-more/$',
        AjaxReviewLoadMoreView.as_view(), name='review-load-more'),
    
    url(r'^article-share/$',
        ArticleShareView.as_view(), name='article-share'),

    url(r'^article-comment/$',
        ArticleCommentView.as_view(), name='article-comment-post'),

    url(r'^email-exist/$',
        EmailExistView.as_view(), name='email-exist'),

    url(r'^get-states/$',
        AjaxStateView.as_view(), name='indian-state'),

    # custom admin flow
    url(r'^orderitem/add-comment/$',
        AjaxOrderItemCommentView.as_view(), name='order-item-comment'),

    url(r'^orderitem/approve-draft/$',
        ApproveByAdminDraft.as_view(), name='oi-draft-accept'),

    url(r'^orderitem/reject-draft/$',
        RejectByAdminDraft.as_view(), name='oi-draft-reject'),

    url(r'^orderitem/upload-draft/$',
        UploadDraftView.as_view(), name='oi-draft-upload'),

    url(r'^orderitem/waiting-input-save/$',
        SaveWaitingInput.as_view(), name='oi-waiting-input'),

    url(r'^orderitem/linkedin-approve-draft/$',
        ApproveDraftByLinkedinAdmin.as_view(), name='linkedin-approve-draft'),

    url(r'^orderitem/linkedin-reject-draft/$',
        RejectDraftByLinkedinAdmin.as_view(), name='linkedin-reject-draft'),
]




