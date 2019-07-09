

const continueAsGuest = () => {
    $('#login_form').addClass('hidden');
    $('#guest_form').removeClass('hidden');
    $('#continue-as-guest-button').addClass('hidden');
    $('#login-candidate-button').removeClass('hidden');
    $('#forgot-password-form').addClass('hidden');


};

const loginAsCandidate = () => {
    $('#login_form').removeClass('hidden');
    $('#guest_form').addClass('hidden');
    $('#continue-as-guest-button').removeClass('hidden');
    $('#login-candidate-button').addClass('hidden');
    $('#forgot-password-form').addClass('hidden');


};

const forgotPassword = () => {
    $('#login_form').addClass('hidden');
    $('#guest_form').addClass('hidden');
    $('#forgot-password-form').removeClass('hidden');
}


$().ready(function () {
    $('#login_form').on('submit', function () {
// hitGAContinue();
    });

    $("#login_form").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6,
            },
        },
        messages: {
            email: {required: "Please enter a valid email address",},
            password: {
                required: "Please enter valid password",
            },
        },
        highlight: function (element) {
            $(element).closest('.form-group').addClass('error');
        },
        unhighlight: function (element) {
            $(element).closest('.form-group').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).siblings('.error-txt').html(error.text());
        }
    });

});
