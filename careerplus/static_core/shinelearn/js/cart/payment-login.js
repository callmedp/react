/*
* *
* * basic headers
* */

const defaultHeaders = {
    "Content-Type": "application/json",
};


/*
** @handle basic request flow
* */


async function handleResponse(response, isFetchingHTML) {

    // handle all the status and conditions here
    if (response['ok'] === false) {
        let message = '';
        let data = await response.json();
        for (const key in data) {
            message += `${data[key]} `;
        }
        if (response['status'] === 401) {
            // Handle validation
        }
        return {
            error: true,
            errorMessage: message,
            status: response['status'],
        }
    } else if (response['status'] === 204) {
        return {data: {}};
    } else {
        let result = isFetchingHTML ? await response.text() : await response.json();
        return {data: result};
    }
}


/*
* *
* *  login Candidate using API
* *
* */

const handleLoginCandidate = async () => {

    const formData = $('#login_form').serializeArray().reduce((obj, item) => {
        obj[item.name] = item.value
        return obj;
    }, {});

    formData['withInfo'] = false;

    // delete csrf token as we don't need it while login through drf api.
    if (formData['csrfmiddlewaretoken']) delete formData['csrfmiddlewaretoken'];

    /*
    * return if form is not valid.
    * */
    if (!$('#login_form').valid()) {
        return;
    }

    const loginResponse = await fetch(`${site_domain}/api/v1/candidate-login/`, {
        headers: defaultHeaders,
        method: 'POST',
        body: JSON.stringify(formData)
    });

    const result = await handleResponse(loginResponse)

    console.log('---result---', result);
    if (result['error']) {
        // Todo ***** error handling  *****
        $('#invalid-cred').show().delay(5000).fadeOut()
        return;
    }
    /*
    *  update the cart
    * */

    const updateCartResponse = await fetch(`${site_domain}/api/v1/cart/update/`, {
        headers: defaultHeaders,
        method: 'POST',
        body: JSON.stringify(formData)
    });
};


/*
*  continue as guest option handled
* */
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

/*
*  login as candidate option handled
* */
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

/*
*  forgot password option handled
* */

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


/*
*  login form validation
* */

$(document).ready(function () {

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
            email: {
                required: "Email address is required",
            },
            password: {
                required: "Password is required",
            },
        },
        highlight: function (element) {

            let className = '.form-group', addClass = 'error1';

            if (window.CURRENT_FLAVOUR == 'mobile') {
                className = 'li';
                addClass = 'error'
            }
            $(element).closest(className).addClass(addClass);
        },
        unhighlight: function (element) {

            let className = '.form-group', addClass = 'error1', errorTextClass = '.error-txt';

            if (window.CURRENT_FLAVOUR == 'mobile') {
                className = 'li';
                addClass = 'error'
                errorTextClass = '.error--mgs'
            }
            $(element).closest(className).removeClass(addClass);
            $(element).siblings(errorTextClass).html('');


        },
        errorPlacement: function (error, element) {
            let errorTextClass = '.error-txt';
            if (window.CURRENT_FLAVOUR == 'mobile') {
                errorTextClass = '.error--mgs';
            }
            $(element).siblings(errorTextClass).html(error.text());
        }
    });

});
