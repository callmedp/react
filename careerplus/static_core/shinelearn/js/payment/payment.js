$(document).ready(function () {
    $('#check-sumit-button').click(function () {
        if ($('#check-pay-form').valid()) {
            $('#check-pay-form').submit();
        }
    });

    $.validator.addMethod("validState", function (value, element) {
        var state_id = $('#id_state').val();
        if (state_id != -1) {
            return true;
        }
        return false;
    });

    $("#id-cash-form").validate({
        rules: {
            state: {
                required: true,
                validState: true,
            },
        },
        messages: {
            state: {
                required: 'this value is required.',
                validState: 'Please select valid state.',
            },
        },
    });

    var today = new Date();
    // set end date to max one year period:
    var start = new Date(new Date().setMonth(today.getMonth() - 3));

    var end = new Date(new Date().setYear(today.getFullYear() + 1));


    $('#id_deposit_date').datepicker({
        startDate: start,
        endDate: end,
        format: "dd-mm-yyyy",
        weekStart: 1,
        orientation: "bottom left",
        daysOfWeekHighlighted: "1,2,3,4,5,6",
        autoclose: true,
        todayHighlight: true
    });

    $("#check-pay-form").validate({
        rules: {
            cheque_no: {
                required: true,
                digits: true,
                minlength: 6,
                maxlength: 6,
            },
            drawn_bank: {
                required: true,
            },
            deposit_date: {
                required: true,
            },
        },
        messages: {
            cheque_no: {
                required: 'this field is required.',
                digits: 'enter only digits.',
                minlength: 'length must be 6 digits.',
                maxlength: 'length must be 6 digits.',
            },
            drawn_bank: {
                required: 'this field is required.',
            },
            deposit_date: {
                required: 'this field is required.',
            },
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
            let className = '.form-group', removeClass = 'error1', errorTextClass = '.error-txt';
            if (window.CURRENT_FLAVOUR == 'mobile') {
                className = 'li';
                removeClass = 'error'
                errorTextClass = '.error--mgs'
            }
            $(element).closest(className).removeClass(removeClass);
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

    $(".input-effect input").val("");

    $(".input-effect input").focusout(function () {
        if ($(this).val() != "") {
            $(this).addClass("has-content");
        } else {
            $(this).removeClass("has-content");
        }
    })


 $('#headingThree').click(function(){
 $('#zest_emi_div').show();
 $("#emi-block-0" ).hide();
 $("#emi-block-1" ).hide();
      $.ajax({
        url: '/payment/api/zest-money/emi-plans/',
        type: 'get',
        data: {'amount' :totalAmount },
        dataType: 'json',
        success: function(data) {
            if (data.length > 0) {;
                $("#zest-emi-head").text("EMI Options");
                $.each(data, function(index, plan) {
                    $("#emi-" + index + "-months").text("No. Of Months : " + plan['number_of_months']);
                    $("#emi-" + index + "-monthly-amount").text("Monthly Amount : " + (plan['total_monthly_amount'] - plan['interest_amount'] / plan['number_of_months']));
                    $("#emi-" + index + "-interest").text("Interest : " + plan['interest_amount']);
                    $("#emi-" + index + "-interest-rate").text("Interest rate : " + plan['interest_rate']);
                    $("#emi-" + index + "-down-payment").text("Down Payment : " + plan['down_payment_amount']);
                    $("#emi-" + index + "-total-amount").text("Loan Amount : " + (plan['loan_amount']));
                    $("#emi-block-" + index ).show();
                });
            }
        },
        failure: function() {
            $(".zest_emi_div").hide();
        }
    });

 })


 $('#zestMakePaymentBtn').click(function(){
 $.get( "/payment/zestmoney/request/"+cart_id+'/', function(data) {
 if(hasOwnProperty.call(data, 'url')){
 window.location.replace(data.url);
 }
})
  .done(function(data) {
    $('#containerBlock').html(`
    <html>
<head>
    <title>Redirecting to Zest Money for Payment</title>
</head>
<body>
    <h3>Redirecting to Payment gateway. Please do not Refresh or close this window.</h3>
</body>
    `)
  })
  .fail(function(data) {
    alert( "Error in making a request" );
  })
 })

});