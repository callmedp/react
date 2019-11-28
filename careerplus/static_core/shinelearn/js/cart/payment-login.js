

$(document).ready(function () {
    /*
    * validate login form
    * */

    $('.trig-loader').click(function () {
        $('.overlay-background').show()
        $('body').addClass('body-noscroll')
    })

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

    /*
    *  validate forget
     *  */

    $("#forgot_form_1").validate({
        submitHandler: function (form) {
            let formData = $(form).serialize();
            let post_url = $(form).attr('action');
            $.ajax({
                url: post_url,
                type: "POST",
                data: formData,
                dataType: 'json',
                success: function (json) {
                    if (json.exist == true) {
                        $("#forgot_form_1")[0].reset();
                        $('#forgot_div').modal('hide');
                        $('#forgot_form_1').addClass('hidden');
                        $('#login_form').removeClass('hidden');
                        Swal.fire({
                            title: 'Success!',
                            text: 'Link has been sent to your registered email id',
                            type: 'success',
                            showConfirmButton: false,
                            timer: 1500
                        })
                        if (json.next != '') {
                            window.location.href = json.next;
                        }

                    } else if (json.notexist == true) {
                        Swal.fire({
                            title: 'Error!',
                            text: 'Your email is not registered on shine learning. Please enter the register email',
                            type: 'error',
                            showConfirmButton: false,
                            timer: 2000

                        })
                    } else if (json.noresponse == true) {
                        Swal.fire({
                            title: 'Error!',
                            text: 'Something went wrong. Try again later',
                            type: 'error',
                            showConfirmButton: false,
                            timer: 2000

                        })
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    Swal.fire({
                        title: 'Error!',
                        text: 'Something went wrong. Try again later',
                        type: 'error',
                        showConfirmButton: false,
                        timer: 2000

                    })
                }
            });
        },
        rules: {
            email: {
                required: true,
                email: true,
            }
        },
        messages: {
            email: { required: "Email address is required." },
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



    /*
* *
* * basic headers
* */
});

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
})

/*
** @handle basic request flow
* */

const defaultHeaders = {
    "Content-Type": "application/json",
};

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
        return { data: {} };
    } else {
        let result = isFetchingHTML ? await response.text() : await response.json();
        return { data: result };
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
    $('.overlay-background').show()
    $('body').addClass('body-noscroll')

    loginResponse = await fetch(`${site_domain}/api/v1/candidate-login/`, {
        headers: defaultHeaders,
        method: 'POST',
        body: JSON.stringify(formData)
    })

    let result;

    result = await handleResponse(loginResponse)

    

    if (result['error']) {
        // Todo ***** error handling  *****
        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
        $('#invalid-cred').show().delay(5000).fadeOut()

        return;
    }
    const { data: { candidate_id, cart_pk, token, profile: { email, first_name, last_name, cell_phone, country_code } } } = result;

    /*
    *  update the cart
    * */
    const updatedInfo = {
        'email': email,
        'owner_id': candidate_id,
        'owner_email': email,
        'first_name': first_name,
        'last_name': last_name,
        'mobile': cell_phone,
        'country_code': country_code
    }
    
    if (!cart_pk) {
        window.location.href = '/logout/';
    } 
    
    const updateCartResponse = await fetch(`${site_domain}/api/v1/cart/${cart_pk}/`, {
        headers: defaultHeaders,
        method: 'PUT',
        body: JSON.stringify(updatedInfo)
    });

    const cartData = await handleResponse(updateCartResponse);



    if (cartData['error']) {
        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
        // Todo ***** error handling  *****
        Toast.fire({
            type: 'error',
            title: cartData['error']
        })
        window.location.href = '/logout/';
        return;
    }
    // $('.overlay-background').hide()
    // $('body').removeClass('body-noscroll')

    window.location.href = `/payment/payment-options/`;

};

/*
* handle forgot password
* */

const handleForgotPassword = async () => {

    /*
   * return if form is not valid.
   * */
    if (!$('#forgot_form_1').valid()) {
        return;
    }

    $('#forgot_form_1').submit()
}



/*
*  continue as guest option handled
* */
const continueAsGuest = () => {
    $('#login_form').addClass('hidden');
    // $('#login_form').trigger('reset');
    $('#guest_form').removeClass('hidden');
    $('#continue-as-guest-button').addClass('hidden');
    $('#login-candidate-button').removeClass('hidden');
    $('#forgot_form_1').addClass('hidden');
    // $('#forgot_form_1').trigger('reset');
    $('#forgot_form').addClass('hidden');
    // $('#forgot_form').trigger('reset');
    $('#user_payment_login').addClass('hide');
    $('#guest_payment_login').removeClass('hide')
    $('#login_users').addClass('hide');
    $('#login_guests').removeClass('hide');
    $('#continue-as-guest-button').removeClass('forget-password');
};

/*
*  login as candidate option handled
* */
const loginAsCandidate = () => {
    $('#login_form').removeClass('hidden');
    $('#guest_form').addClass('hidden');
    // $('#guest_form').trigger('reset');
    $('#continue-as-guest-button').removeClass('hidden');

    $('#login-candidate-button').addClass('hidden');
    $('#forgot_form_1').addClass('hidden');
    // $('#forgot_form_1').trigger('reset');
    $('#forgot_form').addClass('hidden');
    // $('#forgot_form').trigger('reset');
    $('#user_payment_login').removeClass('hide');
    $('#guest_payment_login').addClass('hide');
    $('#user-forgot-password').addClass('hide');
    $('#login_users').removeClass('hide');
    $('#login_guests').addClass('hide');
    $('#continue-as-guest-button').removeClass('forget-password');


};

/*
*  forgot password option handled
* */

const forgotPassword = () => {
    $('#login_form').addClass('hidden');
    // $('#login_form').trigger('reset');
    $('#guest_form').addClass('hidden');
    // $('#guest_form').trigger('reset');
    $('#login_users').addClass('hide');
    $('#login_guests').addClass('hide');
    $('#user_payment_login').addClass('hide');
    $('#guest_payment_login').addClass('hide');
    $('#user-forgot-password').removeClass('hide');
    $('#continue-as-guest-button').addClass('forget-password');
    $('#forgot_form_1').removeClass('hidden');
    $('#forgot_form').removeClass('hidden');
}


/*
*  login form validation
* */
