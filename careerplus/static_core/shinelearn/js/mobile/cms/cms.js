var highlightError = function(element, errorClass) {
    $(element).siblings('.mgs').show();
    $(element).closest('.form-group').addClass('error');
};

var unhighlightError = function(element, errorClass) {
    $(element).siblings('.mgs').hide();
    $(element).closest('.form-group').removeClass('error');
};

var errorPlacement = function(error, element){
    $(element).siblings('.mgs').html(error.text());
};

var showLeadForm = function () {
    // do nothing
};

$(document).ready(function() {
    $(document).on('click', '.js_redirect', function(event) {
        window.location.href = window.MOBILE_LOGIN_URL + "?next="+window.location.pathname;
    });
});
