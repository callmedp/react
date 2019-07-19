

const continueAsGuest = () => {
    $('#login_form').addClass('hidden');
    $('#guest_form').removeClass('hidden');
    $('#continue-as-guest-button').addClass('hidden');
    $('#login-candidate-button').removeClass('hidden');
    $('#forgot_form').addClass('hidden');
    $('#user_payment_login').addClass('hide');
    $('#guest_payment_login').removeClass('hide')
    $('#login_users').addClass('hide');
    $('#login_guests').removeClass('hide');



};

const loginAsCandidate = () => {
    $('#login_form').removeClass('hidden');
    $('#guest_form').addClass('hidden');
    $('#continue-as-guest-button').removeClass('hidden');
    $('#login-candidate-button').addClass('hidden');
    $('#forgot_form').addClass('hidden');
    $('#user_payment_login').removeClass('hide');
    $('#guest_payment_login').addClass('hide');
    $('#user-forgot-password').addClass('hide');
    $('#login_users').removeClass('hide');
    $('#login_guests').addClass('hide');



};

const forgotPassword = () => {
    $('#login_form').addClass('hidden');
    $('#guest_form').addClass('hidden');
     $('#login_users').addClass('hide');
    $('#login_guests').addClass('hide');
     $('#user_payment_login').addClass('hide');
    $('#guest_payment_login').addClass('hide');
    $('#user-forgot-password').removeClass('hide');
    $('#forgot_form').removeClass('hidden');

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
            $(element).closest('li').addClass('error');
        },
        unhighlight: function (element) {
            $(element).closest('li').removeClass('error');
            $(element).siblings('.error--mgs').html('');

        },
        errorPlacement: function (error, element) {
            $(element).siblings('.error--mgs').html(error.text());
        }
    });

});
