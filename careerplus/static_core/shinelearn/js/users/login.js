var googleRedirectionUrl;
window.fbAsyncInit = function () {
    FB.init({
        appId: '1482454715170390', // App ID
        status: true, // check login status
        cookie: true, // enable cookies to allow the server to access the session
        xfbml: true, // parse XFBML
        version: 'v2.10',
    });
};

function Login(redirect_url) {
    if (redirect_url == undefined) {
        redirect_url = "/";
    }
    FB.login(function (response) {
        if (response.status == 'connected') {
            ajaxCallSocialLogin(response.authResponse.accessToken, response.authResponse.expiresIn, 'fb', redirect_url)
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {scope: 'email'});
}

// Load the SDK asynchronously
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v2.10&appId=1482454715170390";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Social Gplus Login

function loginCallback(result) {

    if (result['status']['signed_in']) {
        ajaxCallSocialLogin(result.access_token, result.expires_in, 'gplus', googleRedirectionUrl)
    }
}


function glogin(redirect_url) {
    if (redirect_url == undefined) {
        redirect_url = "/";
    }
    googleRedirectionUrl = redirect_url;
    var myParams = {
        'clientid': '653414155457-ufec3m78n4ctcvfqn34jf8skn4mv909e.apps.googleusercontent.com',
        'cookiepolicy': 'single_host_origin',
        'callback': 'loginCallback', //callback function
        'approvalprompt': 'force',
        'scope': 'profile email',
    };
    gapi.auth.signIn(myParams);
}

var auth2;
var startApp = function () {
    gapi.load('auth2', function () {
        /* Retrieve the singleton for the GoogleAuth library and set up the client.*/
        auth2 = gapi.auth2.init({
            client_id: '653414155457-ufec3m78n4ctcvfqn34jf8skn4mv909e.apps.googleusercontent.com',
            cookiepolicy: 'single_host_origin',
            /* Request scopes in addition to 'profile' and 'email'*/
            scope: 'profile email'
        });
    });
};

(function () {
    var po = document.createElement('script');
    po.type = 'text/javascript';
    po.async = true;
    po.src = 'https://apis.google.com/js/client.js?onload=startApp';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(po, s);
})();


function validate_linkedin_login_terms() {
    if ($('#accept-condition').is(":checked")) {
        var mobile_attr = $('#linkedin_url_id').attr('mobile');
        if (mobile_attr == 'mobile') {
            $('.bs-example-modal-sm-linkedin').modal('show');
            return false;
        } else {
            return true;
        }
    } else {
        $('#term-error').text('Please agree the terms and conditions.');
        return false
    }
}

function saveReviewFormDataToLocalStorage() {
    var formData = $('#feedback-form').serialize();
    if (formData) {
        localStorage.setItem('formData', formData);
    }
}

function googleLoginCallback(result) {

    if (result['status']['signed_in']) {
        saveReviewFormDataToLocalStorage()
        ajaxCallSocialLogin(result.access_token, result.expires_in, 'gplus', window.location.href)
    }
}

function reviewSocialLogin(next_url = undefined, social_id) {
    if (social_id == 'fb') {
        FB.login(function (response) {
            if (response.status == 'connected') {
                saveReviewFormDataToLocalStorage()
                ajaxCallSocialLogin(response.authResponse.accessToken, response.authResponse.expiresIn, 'fb', next_url)
            } else {
                console.log('User cancelled login or did not fully authorize.');
            }
        }, {scope: 'email'});
    } else if (social_id == 'gplus') {
        var myParams = {
            'clientid': '653414155457-ufec3m78n4ctcvfqn34jf8skn4mv909e.apps.googleusercontent.com',
            'cookiepolicy': 'single_host_origin',
            'callback': 'googleLoginCallback', //callback function
            'approvalprompt': 'force',
            'scope': 'profile email',
        };
        gapi.auth.signIn(myParams);
    }

}

function ajaxCallSocialLogin(accessToken, expiresIn, social_id, next_url = undefined) {
    var sign_in_url = '/user/social/login/?accessToken=' + accessToken + '&expiresIn=' + expiresIn + '&key=' + social_id;
    if (next_url) {
        sign_in_url = sign_in_url + '&next_url=' + next_url;
    }
    window.location.href = sign_in_url
}

const handleLogin = () => {
    if ($('#login_form').valid()) {
        document.getElementById('login_form').submit();
    }
}

$(document).ready(function () {

    $('#accept-condition').click(function () {
        if ($(this).is(":checked")) {
            $('#term-error').text('');
        }
    });

    /*try{
        var mobile_attr = $('#linkedin_url_id').attr('mobile');
        if (mobile_attr == 'mobile') {
            $('.bs-example-modal-sm-linkedin').modal('show');
        }
    }catch(err){
    }*/


    // login and registration js 
    var emailresponse;
    $.validator.addMethod("emailDoesNotExist",
        function (value, element) {
            $.ajax({
                type: "GET",
                async: false,
                url: "/ajax/email-exist/",
                data: {email: $("#id_email").val()},
                success: function (res) {
                    emailresponse = res.exists;
                }
            });
            return emailresponse;

        },
        "This email id does not exists."
    );
    $("#login_form").validate({
        submitHandler: function (form) {
            debugger;
            form.submit();
            // e.preventDefault();
            /*if($(this).val() != '')
            {
              $('button[type="submit"]').prop('disabled', false);  
            }
            else
            {
              $('button[type="submit"]').prop('disabled', true);
            } */
        },
        rules: {
            email: {
                required: true,
                email: true/*,
                    emailDoesNotExist:true*/

            },
            password: {
                required: true,
                minlength: 6,
                maxlength: 15
            }
        },
        messages: {
            email: {required: "Please enter a valid email address."},
            password: {
                required: "Please provide a password"
            }
        },
        highlight: function (element, errorClass) {
            $(element).closest('.form-group').addClass('error');
        },
        unhighlight: function (element, errorClass) {
            $(element).closest('.form-group').removeClass('error');
            $(element).siblings('.error-txt').html('');
        },
        errorPlacement: function (error, element) {
            $(element).siblings('.error-txt').html(error.text());
        },
    });

    $.validator.addMethod("indiaMobile", function (value, element) {
        var country_code = $('#id_country_code').val();
        if (country_code == '91') {
            return value.length == 10;
        }
        return true;
    });

    $("#linkedin-form-id").validate({
        rules: {
            mobile: {
                required: true,
                number: true,
                indiaMobile: true,
                minlength: 6,
                maxlength: 15
            }
        },
        messages: {
            mobile: {
                required: "Please enter valid mobile number",
                number: "Enter only numbers",
                indiaMobile: "Length must be 10 digits.",
                maxlength: "Please enter up to 15 digits",
                minlength: "Please enter at least 6 digits",
            },
        },
        highlight: function (element, errorClass) {
            $(element).closest('.form-group').addClass('error');
            $(element).siblings('.js-error').addClass('error-txt');
        },
        unhighlight: function (element, errorClass) {
            $(element).closest('.form-group').removeClass('error');
            $(element).siblings('.js-error').removeClass('error-txt');
            $(element).siblings('.js-error').html('');
        },
        errorPlacement: function (error, element) {
            $(element).siblings('.js-error').html(error.text());
        },

    });

    $("#forgot_form").validate({
        submitHandler: function (form) {
            debugger;
            var formData = $(form).serialize();
            var post_url = $(form).attr('action');
            $('#forgot_div').modal('hide');
            $('#forgot_form').addClass('hidden');
            $('#login_form').removeClass('hidden');
            $.ajax({
                url: post_url,
                type: "POST",
                data: formData,
                dataType: 'json',
                success: function (json) {
                    $("#forgot_form")[0].reset();
                    if (json.exist == true) {
                        alert('Link has been sent to your registered email id');
                        // $("#msg_for_user").html("Link has been sent to your registered email id").show();
                        // $('#forgot_div').modal('show');
                    } else if (json.notexist == true) {
                        $("#msg_for_user").html("your email does not exist on shine learning").show();
                        $('#forgot_div').modal('show');
                    } else if (json.noresponse == true) {
                        $("#msg_for_user").html("Something went wrong. Try again later").show();
                        $('#forgot_div').modal('show');
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong. Try again later");
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
            email: {required: "Please enter a valid email address."},
        },
        highlight: function (element, errorClass) {
            $(element).closest('li').addClass('error');
        },
        unhighlight: function (element, errorClass) {
            $(element).closest('li').removeClass('error');
            $(element).siblings('.error--mgs').html('');
        },
        errorPlacement: function (error, element) {
            $(element).siblings('.error--mgs').html(error.text());
        },
    });
    // end login and registration js

    $('#modalforgot').click(function () {
        $('#forgot_div').modal('show');
        $("label#id_email-error.error").remove();
        $("#msg_for_user").hide();
    });
});