
$(document).ready(function() {
    $(document).on('click', '.js_redirect', function(event) {
        window.location.href = window.MOBILE_LOGIN_URL + "?next="+window.location.pathname;
    });
});
