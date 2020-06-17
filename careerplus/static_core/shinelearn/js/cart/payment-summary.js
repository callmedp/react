function toggler(divId, show_hide_coupon) {
    if (show_hide_coupon) {
        var ele = $("#show_hide_coupon")
        var text = ele.text()
        if (text == 'Apply coupon') {
            ele.text('Hide Coupon')
        } else {
            ele.text('Apply coupon')
        }
    }
    $("#" + divId).toggle();
}

function JSApplyDiscount(e) {
    var attr = $('#discount-apply').attr('disabled');
    if (typeof attr !== typeof undefined && attr !== false) {
        e.preventDefault();
        return;
    }

    $('#discount-apply').prop('disabled', true);

    // show loader
    $('.overlay-background').show()
    $('body').addClass('body-noscroll')

    var alert_message = '';
    if ($('#discount_code').val().trim()) {
        $('#discount_code').parent().removeClass('error');
        try {
            var discount_code = $('#discount_code').val().trim();
            $.ajax({
                url: '/cart/applycoupon/',
                type: 'post',
                data: 'code=' + discount_code,
                dataType: 'json',
                success: function (json) {
                    window.location.reload();
                },
                failure: function (response) {
                    alert_message = 'Something is not working, Please try later!';

                    // remove loader
                    $('.overlay-background').hide()
                    $('body').removeClass('body-noscroll')

                    $('#discount_code').parent().addClass('error');
                    $('#discount-alert').empty();
                    $('#discount-alert').text(alert_message);
                    $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
                    $('#discount-apply').prop('disabled', false);


                },
                error: function (result, status, err) {
                    if (result && result.status == 400) {
                        alert_message = result.responseJSON;
                        alert_message = alert_message.error;
                    } else {
                        alert_message = 'Something is not working, Please try later!';

                    }
                    // remove loader
                    $('.overlay-background').hide()
                    $('body').removeClass('body-noscroll')

                    $('#discount_code').parent().addClass('error');
                    $('#discount-alert').empty();
                    $('#discount-alert').text(alert_message);
                    $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
                    $('#discount-apply').prop('disabled', false);


                }
            });
        } catch (e) {
            alert_message = 'Something is not working, Please try later!';

            // remove loader
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')
            $('#discount_code').parent().addClass('error');
            $('#discount-alert').empty();
            $('#discount-alert').text(alert_message);
            $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);

        }

    } else {
        alert_message = 'Enter Discount Code First!';
        // remove loader
        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
        $('#discount_code').parent().addClass('error');
        $('#discount-alert').empty();
        $('#discount-alert').text(alert_message);
        $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
        $('#discount-apply').prop('disabled', false);


    }
};

function JSApplyPoint(e) {
    var attr = $('#loyalty-point-apply').attr('disabled');
    if (typeof attr !== typeof undefined && attr !== false) {
        e.preventDefault();
        return;
    }

    $('#loyalty-point-apply').prop('disabled', true);
    // show loader
    $('.overlay-background').show()
    $('body').addClass('body-noscroll')

    var alert_message = '';
    if ($('#loyalty_point').val().trim()) {
        $('#loyalty_point').parent().removeClass('error');
        try {
            var loyalty_point = $('#loyalty_point').val().trim();
            if (isNaN(loyalty_point)) {
                throw "NaN"
            }
            loyalty_point = parseInt(loyalty_point, 10);
            var min_point = parseInt($('#loyalty_point').prop('min'), 10);
            var max_point = parseInt($('#loyalty_point').prop('max'), 10);
            if (loyalty_point <= min_point) {
                throw "Min"
            }
            if (loyalty_point > max_point) {
                throw "Max"
            }
            $.ajax({
                url: '/cart/applypoint/',
                type: 'post',
                data: 'point=' + loyalty_point,
                dataType: 'json',
                success: function (json) {
                    window.location.reload();
                },
                failure: function (response) {
                    alert_message = 'Something is not working, Please try later!';
                    // remove loader
                    $('.overlay-background').hide()
                    $('body').removeClass('body-noscroll')

                    $('#loyalty_point').parent().addClass('error');
                    $('#point-alert').empty();
                    $('#point-alert').text(alert_message);
                    $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
                    $('#loyalty-point-apply').prop('disabled', false);

                },
                error: function (result, status, err) {
                    if (result && result.status == 400) {
                        alert_message = result.responseJSON;
                        alert_message = alert_message.error;
                    } else {
                        alert_message = 'Something is not working, Please try later!';
                    }

                    // remove loader
                    $('.overlay-background').hide()
                    $('body').removeClass('body-noscroll')

                    $('#loyalty_point').parent().addClass('error');
                    $('#point-alert').empty();
                    $('#point-alert').text(alert_message);
                    $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
                    $('#loyalty-point-apply').prop('disabled', false);

                }
            });
        } catch (e) {
            if (e == 'NaN') {
                alert_message = 'Please enter digits!';
            } else if (e == 'Min') {
                alert_message = 'Redeem points should be greater than 0!';
            } else if (e == 'Max') {
                alert_message = 'Redeem points should be less than available points!';
            } else {
                alert_message = 'Something is not working, Please try later!';
            }

            // remove loader
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')

            $('#loyalty_point').parent().addClass('error');
            $('#point-alert').empty();
            $('#point-alert').text(alert_message);
            $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
            $('#loyalty-point-apply').prop('disabled', false);

        }

    } else {
        alert_message = 'Enter Loyalty Point First!';

        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
        $('#loyalty_point').parent().addClass('error');
        $('#point-alert').empty();
        $('#point-alert').text(alert_message);
        $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
        $('#loyalty-point-apply').prop('disabled', false);

    }
};

function JSRemoveDiscount(e) {
    var attr = $('#remove-discount').attr('disabled');
    if (typeof attr !== typeof undefined && attr !== false) {
        e.preventDefault();
        return;
    }
    $('#remove-discount').prop('disabled', true);

    $('.overlay-background').show()
    $('body').addClass('body-noscroll')

    $.ajax({
        url: '/cart/removecoupon/',
        type: 'post',
        dataType: 'json',
        success: function (json) {
            window.location.reload();
        },
        failure: function (response) {



            alert_message = 'Something is not working, Please try later!';

            // remove loader
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')

            $('#discount_code').parent().addClass('error');
            $('#discount-alert').empty();
            $('#discount-alert').text(alert_message);
            $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
            $('#remove-discount').prop('disabled', false);


        },
        error: function (result, status, err) {



            if (result && result.status == 400) {
                alert_message = result.responseJSON;
                alert_message = alert_message.error;
            } else {
                alert_message = 'Something is not working, Please try later!';

            }

            // remove loader
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')


            $('#discount_code').parent().addClass('error');
            $('#discount-alert').empty();
            $('#discount-alert').text(alert_message);
            $('#discount-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
            $('#remove-discount').prop('disabled', false);


        }
    });

};

function JSRemovePoint(e) {
    var attr = $('#remove-point').attr('disabled');
    if (typeof attr !== typeof undefined && attr !== false) {
        e.preventDefault();
        return;
    }
    $('#remove-point').prop('disabled', true);
    // add loader
    $('.overlay-background').show()
    $('body').addClass('body-noscroll')
    $.ajax({
        url: '/cart/removepoint/',
        type: 'post',
        dataType: 'json',
        success: function (json) {
            window.location.reload();
        },
        failure: function (response) {
            // remove loader
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')
            alert_message = 'Something is not working, Please try later!';
            $('#loyalty_point').parent().addClass('error');
            $('#point-alert').empty();
            $('#point-alert').text(alert_message);
            $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
            $('#remove-point').prop('disabled', false);



        },
        error: function (result, status, err) {
            // remove loader
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')

            if (result && result.status == 400) {
                alert_message = result.responseJSON;
                alert_message = alert_message.error;
            } else {
                alert_message = 'Something is not working, Please try later!';

            }
            $('#loyalty_point').parent().addClass('error');
            $('#point-alert').empty();
            $('#point-alert').text(alert_message);
            $('#point-alert').fadeIn('slow').fadeTo('fast', 0.5).fadeTo('fast', 1.0);
            $('#remove-point').prop('disabled', false);


        }
    });

};

const removalAjax = (formData) => {
    $.ajax({
        url: '/cart/remove-from-cart/',
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: function (json) {
            if (json.status == 1) {
                window.location.reload();
                //alert("product removed from cart successfully");
            } else if (json.status == -1) {
                //remove loader
                $('.overlay-background').hide()
                $('body').removeClass('body-noscroll')
                alert('Something went wrong, Please try again.');
            }
        },
        failure: function (response) {
            // remove loader

            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')

            alert("Something went wrong, Please try again")
        },
        error: function (xhr, ajaxOptions, thrownError) {
            // remove loader
            $('.overlay-background').hide()
            $('body').removeClass('body-noscroll')
            alert("Something went wrong, Please try again")
        }
    });
}

function removeFromCart(line_id) {
    $('.overlay-background').show()
    $('body').addClass('body-noscroll')

    if (line_id) {
        $('#id-remove-cart' + line_id).addClass('disabled').removeAttr("onclick");
        var formData = $('#cart_remove_form' + line_id).serialize();
        removalAjax(formData)

    }
    else {
        // remove loader
        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
    }

};

function removeVariationsOrAddons(csrfToken, reference, lineId) {
    $('.overlay-background').show()
    $('body').addClass('body-noscroll')
    if (lineId) {
        let formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('reference_id', reference);
        removalAjax(formData)
    }
    else {
        // remove loader
        $('.overlay-background').hide()
        $('body').removeClass('body-noscroll')
    }

}


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

const handleError = (prodId) => {
    $('.overlay-background').hide()
    $('body').removeClass('body-noscroll')

    if (prodId) {
        window.location.href = `/login/?next=/cart/payment-summary/?prod_id=${prodId}`;
        return;
    }
    else {
        window.location.href = `/login/?next=/cart/payment-summary/`;
        return;
    }

}



$(document).ready(function () {
    const handPaymentSummary = async () => {

        const defaultHeaders = {
            "Content-Type": "application/json",
        };



        const urlParams = new URLSearchParams(window.location.search);

        const token = urlParams.get('token');
        const prodId = urlParams.get('prod_id');

        const domain = window.location.hostname != 'localhost' && window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '') || 'http://127.0.0.1:8000'
        let loginResponse, responseData;
        if (token) {
            $('.overlay-background').show()
            $('body').addClass('body-noscroll')
            const loginData = { alt: token };
            try {
                loginResponse = await fetch(`${domain}/api/v1/candidate-login/`, {
                    headers: defaultHeaders,
                    method: 'POST',
                    body: JSON.stringify(loginData)
                })
            }
            catch (e) {
                handleError(prodId)
            }

            responseData = await handleResponse(loginResponse)

            if (responseData['error']) {
                // Todo ***** error handling  *****
                handleError(prodId)
            }
        }

        if (prodId) {

            $.ajax({
                url: '/cart/add-to-cart/',
                type: 'POST',
                data: { 'prod_id': prodId, 'cart_type': 'cart', },
                dataType: 'json',
                success: function (json) {
                    if (json.status == 1) {

                        window.location.href = json.cart_url;

                    }
                    else if (json.status == -1) {
                        alert("Something went wrong, Please try again.");
                    }

                },
                failure: function (response) {
                    alert("Something went wrong, Please try again");

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    alert("Something went wrong, Please try again");
                }
            });

        }


        $('#payment-summary-continue-id').click(function () {
            $('#payment-summary-continue-id').attr('disabled', true);
        });

        $('.trig-loader').click(function () {

            $('.overlay-background').show()
            $('body').addClass('body-noscroll')
        })

        $("#discount_code").keyup(function (event) {
            event.preventDefault()
            if (event.keyCode === 13) {
                $("#discount-apply").click();
            }
        });

        $("#loyalty_point").keyup(function (event) {
            event.preventDefault()
            if (event.keyCode === 13) {
                $("#loyalty-point-apply").click();
            }
        });

    }
    handPaymentSummary();
});