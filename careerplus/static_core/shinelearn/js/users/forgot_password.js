$(document).ready(function () {
    $("#forgot_form").validate({
        submitHandler: function (form) {
            var formData = $(form).serialize();
            var post_url = $(form).attr('action');
            $.ajax({
                url: post_url,
                type: "POST",
                data: formData,
                dataType: 'json',
                success: function (json) {

                    console.log('--JSON--',json);
                    if (json.exist == true) {
                        Swal.fire({
                            title: 'Success!',
                            text: 'Link has been sent to your registered email id',
                            type: 'success',
                            showConfirmButton: false,
                            timer: 1500
                        })
                        $("#forgot_form")[0].reset();
                        loginAsCandidate()


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
            email: {required: "Email address is required."},
        },
        highlight: function (element, errorClass) {

            let className = '.form-group', addClass = 'error1';

            if (window.CURRENT_FLAVOUR == 'mobile') {
                className = 'li';
                addClass = 'error'
            }
            $(element).closest(className).addClass(addClass);
        },
        unhighlight: function (element, errorClass) {
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
        },
    });
});